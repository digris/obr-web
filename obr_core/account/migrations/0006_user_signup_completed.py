# Generated by Django 3.2 on 2021-05-19 11:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0005_settings"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="signup_completed",
            field=models.BooleanField(default=False),
        ),
    ]