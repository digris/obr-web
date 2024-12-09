# Generated by Django 5.0.7 on 2024-12-02 08:17

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="QRRedirect",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated", models.DateTimeField(auto_now=True, db_index=True)),
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
                ("target_url", models.CharField(max_length=255)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]