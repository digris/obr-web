# Generated by Django 4.1.3 on 2023-05-03 16:21

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0035_settings_debug_enabled"),
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
                    ("api_master_download", "API - Download media master files"),
                ),
            },
        ),
    ]