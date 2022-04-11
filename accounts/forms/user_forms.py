from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from accounts.models.user import MinorUser


class MinorUserCreationForm(forms.ModelForm):
    """"
        A form for creating new users. Includes all the required fields, plus
    a repeated password.
    """
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput)

    class Meta:
        model = MinorUser
        fields = ('email', 'date_of_birth')

    def clean_password2(self):
        # Check that the two password entries match
        password1, password2 = self.cleaned_data.get(
            "password1"), self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

    def save(self, commit=True):
        # save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password1"))
        if commit:
            user.save()
        return user


class MinorUserChangeForm(forms.ModelForm):
    """
    A form updating users. Includes all the fields on the user, but replaces the
    password field with admin's disabled password hash display
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MinorUser
        fields = (
            'email',
            'password',
            'date_of_birth',
            'is_active',
            'is_admin')


class MinorUserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = MinorUserChangeForm
    add_form = MinorUserCreationForm

    # The fields to be used in displaying the user model.
    list_display = ('email', 'date_of_birth', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Personal info', {"fields": ('date_of_birth',)}),
        ('Permissions', {'fields': ('is_admin',)})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'date_of_birth', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(MinorUser, MinorUserAdmin)
# ... and, since we're not using built-in permissions,
# admin.site.unregister(Group)
