from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Listing Routes
    path('listing/new/', views.create_listing, name='create_listing'),
    path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('listing/<int:pk>/edit/', views.update_listing, name='update_listing'),
    path('listing/<int:pk>/delete/', views.delete_listing, name='delete_listing'),
	path('profile/', views.profile_view, name='profile'),
	path('listing/<int:pk>/message/', views.send_message, name='send_message'),
	path('inbox/', views.inbox_view, name='inbox'),
   path('messages/reply/<int:pk>/', views.reply_message, name='reply_message'),
]