# Generated by Django 4.2.7 on 2023-12-01 10:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0038_legacyuser_date_joined_legacyuser_date_last_login"),
    ]

    operations = [
        migrations.AddField(
            model_name="legacyuser",
            name="first_name",
            field=models.CharField(blank=True, default="", max_length=64),
        ),
        migrations.AddField(
            model_name="legacyuser",
            name="last_name",
            field=models.CharField(blank=True, default="", max_length=64),
        ),
    ]