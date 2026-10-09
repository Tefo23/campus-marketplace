
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Category, Listing, Message


class CampusMarketplaceSecurityTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create two separate student accounts
        cls.seller = User.objects.create_user(
            username='seller_student',
            password='TestPassword123!'
        )

        cls.buyer = User.objects.create_user(
            username='buyer_student',
            password='TestPassword123!'
        )

        # Create a product category
        cls.category, created = Category.objects.get_or_create(
    name='Textbooks',
    defaults={'slug': 'textbooks'}
)
        # Create a listing owned by the seller
        cls.listing = Listing.objects.create(
            seller=cls.seller,
            title='Python Programming Textbook',
            description='A second-hand programming textbook.',
            price=Decimal('150.00'),
            category=cls.category,
            status='available'
        )

        # Create a message sent from buyer to seller
        cls.message = Message.objects.create(
            listing=cls.listing,
            sender=cls.buyer,
            recipient=cls.seller,
            body='Is this textbook still available?'
        )

    # TEST 1
    def test_homepage_is_accessible(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)

    # TEST 2
    def test_anonymous_user_cannot_create_listing(self):
        response = self.client.get(
            reverse('create_listing')
        )

        self.assertEqual(response.status_code, 302)

    # TEST 3
    def test_anonymous_user_cannot_view_inbox(self):
        response = self.client.get(
            reverse('inbox')
        )

        self.assertEqual(response.status_code, 302)

    # TEST 4
    def test_seller_can_access_edit_page(self):
        self.client.force_login(self.seller)

        response = self.client.get(
            reverse('update_listing', args=[self.listing.pk])
        )

        self.assertEqual(response.status_code, 200)

    # TEST 5
    def test_buyer_cannot_edit_sellers_listing(self):
        self.client.force_login(self.buyer)

        response = self.client.get(
            reverse('update_listing', args=[self.listing.pk])
        )

        self.assertEqual(response.status_code, 302)

    # TEST 6
    def test_buyer_cannot_delete_sellers_listing(self):
        self.client.force_login(self.buyer)

        response = self.client.post(
            reverse('delete_listing', args=[self.listing.pk])
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Listing.objects.filter(pk=self.listing.pk).exists()
        )

    # TEST 7
    def test_get_request_cannot_delete_listing(self):
        self.client.force_login(self.seller)

        response = self.client.get(
            reverse('delete_listing', args=[self.listing.pk])
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Listing.objects.filter(pk=self.listing.pk).exists()
        )

    # TEST 8
    def test_seller_can_delete_own_listing(self):
        self.client.force_login(self.seller)

        response = self.client.post(
            reverse('delete_listing', args=[self.listing.pk])
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Listing.objects.filter(pk=self.listing.pk).exists()
        )

    # TEST 9
    def test_buyer_cannot_reply_to_message_addressed_to_seller(self):
        self.client.force_login(self.buyer)

        response = self.client.post(
            reverse('reply_message', args=[self.message.pk]),
            {'body': 'Unauthorized reply'}
        )

        self.assertEqual(response.status_code, 404)

        self.assertEqual(Message.objects.count(), 1)

    # TEST 10
    def test_seller_can_reply_to_received_message(self):
        self.client.force_login(self.seller)

        response = self.client.post(
            reverse('reply_message', args=[self.message.pk]),
            {'body': 'Yes, the textbook is available.'}
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Message.objects.filter(
                sender=self.seller,
                recipient=self.buyer,
                body='Yes, the textbook is available.'
            ).exists()
        )

    # TEST 11
    def test_seller_cannot_message_themselves(self):
        self.client.force_login(self.seller)

        response = self.client.post(
            reverse('send_message', args=[self.listing.pk]),
            {'body': 'Hello myself'}
        )

        self.assertEqual(response.status_code, 302)

        self.assertEqual(Message.objects.count(), 1)

    # TEST 12
    def test_buyer_cannot_message_sold_listing(self):
        self.listing.status = 'sold'
        self.listing.save()

        self.client.force_login(self.buyer)

        response = self.client.post(
            reverse('send_message', args=[self.listing.pk]),
            {'body': 'Can I buy this?'}
        )

        self.assertEqual(response.status_code, 302)

        self.assertEqual(Message.objects.count(), 1)
