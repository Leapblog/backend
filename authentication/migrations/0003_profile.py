# Generated by Django 4.2.5 on 2023-10-09 09:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import authentication.models


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0002_user_otp"),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("bio", models.TextField(blank=True, max_length=500, null=True)),
                ("address", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=authentication.models.Profile.upload_profile_picture,
                    ),
                ),
                ("college", models.CharField(blank=True, max_length=100, null=True)),
                ("batch", models.IntegerField(blank=True, null=True)),
                (
                    "website_url",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "linkedin_url",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
