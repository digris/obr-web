# Generated by Django 3.2.4 on 2021-06-24 17:53

import datetime

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0020_auto_20210624_0939"),
    ]

    operations = [
        migrations.CreateModel(
            name="Master",
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
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "sync_state",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("running", "Running"),
                            ("completed", "Completed"),
                            ("failed", "Failed"),
                        ],
                        db_index=True,
                        default="pending",
                        max_length=16,
                    ),
                ),
                (
                    "sync_last_update",
                    models.DateTimeField(
                        db_index=True,
                        default=datetime.datetime(
                            1970, 1, 1, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                    ),
                ),
                ("encoding", models.CharField(max_length=4, null=True)),
                (
                    "media",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="master",
                        to="catalog.media",
                    ),
                ),
            ],
            options={
                "verbose_name": "Master",
                "verbose_name_plural": "Masters",
            },
        ),
    ]
