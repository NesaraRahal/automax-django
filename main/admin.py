from django.contrib import admin
from .models import Listing,LikedListing
# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    readonly_fields=('id', 'created_at', 'vin')

class LikedListingAdmin(admin.ModelAdmin):
    pass

admin.site.register(Listing, ListingAdmin)
admin.site.register(LikedListing, LikedListingAdmin)