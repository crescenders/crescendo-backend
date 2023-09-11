from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialApp, SocialToken
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import TokenProxy

from apps.accounts.models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = [
            "email",
        ]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "is_admin",
        ]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    readonly_fields = ["uuid"]
    list_display = ["email", "last_login", "is_admin", "social_accounts"]
    list_filter = ["is_admin"]
    fieldsets = [
        (
            "상세정보",
            {
                "fields": [
                    "uuid",
                    "email",
                    "username",
                ]
            },
        ),
        (
            "권한",
            {
                "fields": [
                    "is_admin",
                ]
            },
        ),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]

    @staticmethod
    def social_accounts(obj):
        return (
            obj.socialaccount_set.all()
            if obj.socialaccount_set.all()
            else "연결된 소셜 계정이 없습니다."
        )


admin.site.register(User, UserAdmin)

admin.site.unregister(Group)
admin.site.unregister(TokenProxy)
admin.site.unregister(EmailAddress)
admin.site.unregister(SocialToken)
admin.site.unregister(SocialApp)
