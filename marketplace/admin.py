from django.contrib import admin
from .models import Category, Listing, Profile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 
                    'seller', 
                    'price', 
                    'category', 
                     'status', 'created_at')

    
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'campus_location')