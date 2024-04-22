from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from referral.models import User
# Register your models here.
@admin.register(User)
class UserAdmin(UserAdmin):
    
    filter_horizontal = ()
    list_display = ('phone_number', 'code')
    ordering = ('phone_number',)
    list_filter = ('phone_number', 'code')

