from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import User,Department,Profile
from django.utils.html import format_html

# Register your models here.
class UserAdmin(UserAdmin):
    list_display =('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    search_fields = ('first_name',)
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

# class UserProfileAdmin(admin.ModelAdmin):
#     def thumbnail(self, object):
#         return format_html('<img src="{}" width="30" style="boader-radius:50%;">'.format(object.profile_picture.url))
#     thumbnail.short_description = 'Profile Picture'
#     list_display = ('thumbnail', 'user', 'city', 'state', 'country')



admin.site.register(Department)
admin.site.register(Profile)
admin.site.register(User, UserAdmin)