# Generated by Django 3.2 on 2021-05-11 16:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0003_auto_20210412_2015"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="first_name",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="last_name",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
