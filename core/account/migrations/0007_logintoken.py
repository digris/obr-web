# Generated by Django 3.2.4 on 2021-06-09 16:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0006_user_signup_completed"),
    ]

    operations = [
        migrations.CreateModel(
            name="LoginToken",
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
                    "uuid",
                    models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
                ),
                (
                    "uid",
                    models.CharField(
                        db_index=True,
                        editable=False,
                        max_length=8,
                        null=True,
                        unique=True,
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        db_index=True, max_length=254, verbose_name="email"
                    ),
                ),
                (
                    "value",
                    models.CharField(
                        db_index=True,
                        editable=False,
                        max_length=6,
                        unique=True,
                        verbose_name="token",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("claimed", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
