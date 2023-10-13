# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin

from .models import BlackListedToken, Profile, User


class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "type")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal Info",
            {"fields": ("email", "first_name", "last_name", "type", "otp")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "display_image",
        "bio",
        "college",
        "batch",
        "website_link",
        "linkedin_link",
    )
    search_fields = ("user__username", "user__email", "college", "batch")
    list_filter = ("college", "batch")

    def display_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50px" height="50px" />'.format(obj.image.url)
            )
        return None

    display_image.short_description = "Profile Picture"

    def website_link(self, obj):
        if obj.website_url:
            return format_html(
                '<a href="{}" target="_blank">{}</a>'.format(
                    obj.website_url, obj.website_url
                )
            )
        return None

    website_link.short_description = "Website"

    def linkedin_link(self, obj):
        if obj.linkedin_url:
            return format_html(
                '<a href="{}" target="_blank">{}</a>'.format(
                    obj.linkedin_url, obj.linkedin_url
                )
            )
        return None

    linkedin_link.short_description = "LinkedIn"


admin.site.register(User, CustomUserAdmin)
admin.site.register(BlackListedToken)
admin.site.register(Profile, ProfileAdmin)
