from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User

# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
                'fields': ('phone_number', 'date_of_birth')
            }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
                'fields': ('phone_number', 'date_of_birth')
            }),
    )