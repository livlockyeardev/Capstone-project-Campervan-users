from .models import Listing
from django.contrib import admin

# Register your models here.


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):

    list_display = ('title', 'slug', 'location')
    search_fields = ['title', 'location']
    list_filter = ('toilet_available', 'noise_level')
    prepopulated_fields = {'slug': ('title',)}
