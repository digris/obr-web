# Generated by Django 4.1.3 on 2023-03-31 08:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0032_theme"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="globalpermissions",
            options={
                "default_permissions": (),
                "managed": False,
                "permissions": (
                    ("api_sync_webhooks", "API - Sync webhooks"),
                    ("api_stats_view", "API - Stats view"),
                    ("api_stats_webhooks", "API - Stats webhooks"),
                    ("api_stats_event_create", "API - Stats create events"),
                ),
            },
        ),
        migrations.AlterField(
            model_name="theme",
            name="css",
            field=models.TextField(blank=True, default="", verbose_name="CSS"),
        ),
    ]