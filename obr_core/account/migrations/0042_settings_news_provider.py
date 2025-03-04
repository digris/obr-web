# Generated by Django 5.0.7 on 2025-02-03 18:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0041_legacyuser_is_listener"),
    ]

    operations = [
        migrations.AddField(
            model_name="settings",
            name="news_provider",
            field=models.CharField(
                blank=True,
                choices=[("", "none"), ("srf", "SRF")],
                db_index=True,
                default="",
                max_length=64,
            ),
        ),
    ]
