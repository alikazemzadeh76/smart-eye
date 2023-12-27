from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.html import format_html

from .forms import UserChangeForm, UserCreationForm

from account_app.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('اطلاعات کاربر', {'fields': ('username', "email", 'password', 'change_password')}),
        # Add 'change_password' here
        ('دسترسی ها', {'fields': ('is_admin',)}),
    )
    readonly_fields = ('change_password',)  # Add 'change_password' here

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', "email", 'password1', 'password2'),
        }),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()

    def change_password(self, obj):
        url = reverse('admin:auth_user_password_change', args=[obj.pk])
        return format_html(
            '<a style="padding: 6px 12px; background-color: #007bff; color: white; border-radius: 5px; text-decoration: none;" href="{}">هدایت به صفحه تغییر رمز</a>',
            url)

    change_password.short_description = 'تغییر رمز عبور'


admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
