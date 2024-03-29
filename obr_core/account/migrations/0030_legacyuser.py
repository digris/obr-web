# Generated by Django 4.1.3 on 2023-01-13 16:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0029_auto_20221125_1929"),
    ]

    operations = [
        migrations.CreateModel(
            name="LegacyUser",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        db_index=True,
                        max_length=254,
                        unique=True,
                        verbose_name="Email address",
                    ),
                ),
                (
                    "obp_id",
                    models.PositiveIntegerField(
                        db_index=True, verbose_name="open broadcast - platform ID"
                    ),
                ),
            ],
        ),
    ]
