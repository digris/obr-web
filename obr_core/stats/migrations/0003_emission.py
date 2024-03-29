# Generated by Django 3.2.10 on 2022-02-09 10:56

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0028_alter_media_duration"),
        ("stats", "0002_auto_20220208_1331"),
    ]

    operations = [
        migrations.CreateModel(
            name="Emission",
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
                    "obj_key",
                    models.CharField(
                        db_index=True, editable=False, max_length=128, null=True
                    ),
                ),
                ("time_start", models.DateTimeField(db_index=True, null=True)),
                ("time_end", models.DateTimeField(db_index=True, null=True)),
                (
                    "playlist",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="archived_emissions",
                        to="catalog.playlist",
                    ),
                ),
            ],
            options={
                "verbose_name": "Emission (archived)",
                "verbose_name_plural": "Emissions (archived)",
                "ordering": ["-time_start"],
                "get_latest_by": "time_start",
            },
        ),
    ]
