from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','phone_number','profile_image','national_id')

admin.site.register(UserProfile, UserProfileAdmin)

# Register your models here.
