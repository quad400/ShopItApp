from django.contrib import admin

from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user','phone','city','country']
    list_filter = ['country']


admin.site.register(UserProfile, UserProfileAdmin)
