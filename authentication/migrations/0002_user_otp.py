# Generated by Django 4.2.5 on 2023-09-29 14:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="otp",
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]