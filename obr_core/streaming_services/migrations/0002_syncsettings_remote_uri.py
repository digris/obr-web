# Generated by Django 5.0.7 on 2025-05-12 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("streaming_services", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="syncsettings",
            name="remote_uri",
            field=models.CharField(blank=True, default="", max_length=256),
        ),
    ]
