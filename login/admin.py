from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        (
            'SupportHub',
            {
                'fields': (
                    'full_name',
                    'phone',
                    'role',
                    'email_verified'
                )
            }
        ),
    )


    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'SupportHub',
            {
                'fields': (
                    'full_name',
                    'phone',
                    'role',
                    'email_verified'
                )
            }
        ),
    )


    list_display = (
        'username',
        'full_name',
        'role',
        'email',
        'is_active'
    )