from django.contrib import admin

from account.models import CustomUser

# Register your models here.

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'is_staff', 'is_active', 'user_type')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('phone_number',)
    ordering = ('phone_number',)
    fieldsets = (
        (None, {'fields': ('phone_number', 'password', 'user_type')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )