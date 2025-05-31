from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'username', 'is_barber', 'is_client', 'is_staff')
    list_filter = ('is_barber', 'is_client', 'is_staff', 'is_superuser')
    ordering = ('email',)
    search_fields = ('email', 'username')

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_client', 'is_barber', 'groups', 'user_permissions')}),
        ('Datas importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_client', 'is_barber')}
        ),
    )

admin.site.register(User, UserAdmin)
admin.site.register(Profile)
