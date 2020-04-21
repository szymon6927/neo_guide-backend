from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _

from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (*UserAdmin.fieldsets, (_('Dodatkowe dane'), {'fields': ('city', 'parish', 'community')}))
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                    'first_name',
                    'last_name',
                    'city',
                    'parish',
                    'community',
                    'is_superuser',
                    'is_staff',
                    'is_active',
                ),
            },
        ),
    )

    list_display = (
        'email',
        'first_name',
        'last_name',
        'city',
        'parish',
        'community',
        'is_superuser',
        'is_staff',
        'is_active',
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
