from django.contrib import admin
from .models import User, Listing, Bid, Comment


class ListingInline(admin.TabularInline):
    model = Listing

class UserAdmin(admin.ModelAdmin):
    inlines = [ListingInline] 


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
