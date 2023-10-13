from django.contrib import admin
from django.utils.html import format_html
from .models import User, BlackListedToken, Profile


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


class BlackListedTokenAdmin(admin.ModelAdmin):
    list_display = ("token",)


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name", "type", "otp")
    search_fields = ("username", "email")
    list_filter = ("type",)
    fieldsets = (
        (
            "Personal Information",
            {"fields": ("username", "email", ("first_name", "last_name"), "password")},
        ),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "type")}),
        ("OTP", {"fields": ("otp",)}),
    )


admin.site.register(User, UserAdmin)
admin.site.register(BlackListedToken, BlackListedTokenAdmin)
admin.site.register(Profile, ProfileAdmin)
