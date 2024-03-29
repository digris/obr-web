# Generated by Django 3.2.10 on 2022-03-11 15:38

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0029_alter_playlist_series_episode"),
        ("stats", "0003_emission"),
    ]

    operations = [
        migrations.CreateModel(
            name="Airplay",
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
                ("time_start", models.DateTimeField(db_index=True, editable=False)),
                ("time_end", models.DateTimeField(db_index=True, editable=False)),
                (
                    "media",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="archived_airplays",
                        to="catalog.media",
                    ),
                ),
            ],
            options={
                "verbose_name": "Airplay (archived)",
                "verbose_name_plural": "Airplays (archived)",
                "ordering": ["-time_start"],
                "get_latest_by": "time_start",
            },
        ),
    ]
