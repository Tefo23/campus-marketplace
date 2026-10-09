from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Listing, Category, Message
from .forms import UserRegisterForm, ListingForm

@login_required
def send_message(request, pk):
    listing = get_object_or_404(Listing, pk=pk)

    if request.method != 'POST':
        return redirect('listing_detail', pk=listing.pk)

    if listing.seller == request.user:
        messages.error(
            request,
            "You cannot send a message to yourself."
        )
        return redirect('listing_detail', pk=listing.pk)

    if listing.status != 'available':
        messages.error(
            request,
            "This item is no longer available."
        )
        return redirect('listing_detail', pk=listing.pk)

    body = request.POST.get('body', '').strip()

    if not body:
        messages.error(
            request,
            "Please enter a message."
        )
        return redirect('listing_detail', pk=listing.pk)

    if len(body) > 2000:
        messages.error(
            request,
            "Your message must be 2000 characters or fewer."
        )
        return redirect('listing_detail', pk=listing.pk)

    Message.objects.create(
        listing=listing,
        sender=request.user,
        recipient=listing.seller,
        body=body
    )

    messages.success(
        request,
        "Message sent to seller successfully!"
    )

    return redirect('listing_detail', pk=listing.pk)

@login_required
def reply_message(request, pk):
    original_message = get_object_or_404(
        Message,
        pk=pk,
        recipient=request.user
    )

    if request.method != 'POST':
        return redirect('inbox')

    body = request.POST.get('body', '').strip()

    if not body:
        messages.error(
            request,
            "Please enter a reply."
        )
        return redirect('inbox')

    if len(body) > 2000:
        messages.error(
            request,
            "Your reply must be 2000 characters or fewer."
        )
        return redirect('inbox')

    Message.objects.create(
        listing=original_message.listing,
        sender=request.user,
        recipient=original_message.sender,
        body=body
    )

    messages.success(
        request,
        "Reply sent successfully!"
    )

    return redirect('inbox')

@login_required
def inbox_view(request):
    received_messages = Message.objects.filter(recipient=request.user)
    sent_messages = Message.objects.filter(sender=request.user)
    return render(request, 'marketplace/inbox.html', {
        'received_messages': received_messages,
        'sent_messages': sent_messages
    })
	
# --- HOME VIEW ---
def home(request):
    listings = Listing.objects.filter(
        status='available'
    ).select_related(
        'category', 'seller'
    ).order_by('-created_at')

    categories = Category.objects.all().order_by('name')

    # Get search and category values from the URL
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()

    # Search for products by title or description
    if query:
        from django.db.models import Q

        listings = listings.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    # Filter products by category
    if category_slug:
        listings = listings.filter(
            category__slug=category_slug
        )

    context = {
        'listings': listings,
        'categories': categories,
        'query': query,
        'selected_category': category_slug,
    }

    return render(request, 'marketplace/index.html', context)


# --- AUTHENTICATION VIEWS ---
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Account created successfully! Welcome, {user.username}.")
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'marketplace/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'marketplace/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')


# --- LISTING VIEWS ---
def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, 'marketplace/listing_detail.html', {'listing': listing})


@login_required
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            messages.success(request, "Your listing has been created successfully!")
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = ListingForm()
    return render(request, 'marketplace/listing_form.html', {'form': form, 'title': 'Create Listing'})


@login_required
def update_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if listing.seller != request.user:
        messages.error(request, "You are not authorized to edit this listing.")
        return redirect('listing_detail', pk=listing.pk)

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, "Listing updated successfully!")
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = ListingForm(instance=listing)
    return render(request, 'marketplace/listing_form.html', {'form': form, 'title': 'Edit Listing'})

@login_required
def profile_view(request):
    user_listings = Listing.objects.filter(
        seller=request.user
    ).select_related('category').order_by('-created_at')

    total_listings = user_listings.count()
    available_listings = user_listings.filter(status='available').count()
    sold_listings = user_listings.filter(status='sold').count()

    context = {
        'listings': user_listings,
        'total_listings': total_listings,
        'available_listings': available_listings,
        'sold_listings': sold_listings,
    }

    return render(request, 'marketplace/profile.html', context)

@login_required
def delete_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)

    if listing.seller != request.user:
        messages.error(
            request,
            "You are not authorized to delete this listing."
        )
        return redirect('listing_detail', pk=listing.pk)

    if request.method != 'POST':
        messages.error(
            request,
            "Listings can only be deleted using the confirmation form."
        )
        return redirect('listing_detail', pk=listing.pk)

    listing.delete()

    messages.success(
        request,
        "Listing deleted successfully!"
    )

    return redirect('profile')