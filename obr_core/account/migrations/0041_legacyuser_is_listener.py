# Generated by Django 4.2.7 on 2023-12-01 10:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0040_legacyuser_gender_legacyuser_phone_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="legacyuser",
            name="is_listener",
            field=models.BooleanField(
                default=False, help_text="has account on radio site"
            ),
        ),
    ]
