# Generated by Django 4.2.2 on 2023-09-11 16:23

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stats", "0008_alter_emission_obj_key"),
    ]

    operations = [
        migrations.CreateModel(
            name="Heartbeat",
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
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("time", models.DateTimeField(db_index=True)),
                ("user_identity", models.CharField(db_index=True, max_length=64)),
                ("device_key", models.CharField(db_index=True, max_length=64)),
                (
                    "user_agent",
                    models.CharField(blank=True, default="", max_length=500),
                ),
                ("in_foreground", models.BooleanField(db_index=True)),
                (
                    "player_source",
                    models.CharField(
                        choices=[("live", "live"), ("ondemand", "ondemand")],
                        db_index=True,
                        max_length=16,
                    ),
                ),
                (
                    "player_state",
                    models.CharField(
                        choices=[
                            ("playing", "playing"),
                            ("stopped", "stopped"),
                            ("paused", "paused"),
                            ("buffering", "buffering"),
                        ],
                        db_index=True,
                        max_length=16,
                    ),
                ),
            ],
            options={
                "verbose_name": "Heartbeat",
                "db_table": "stats_heartbeat",
                "ordering": ["-time"],
                "unique_together": {("user_identity", "device_key")},
            },
        ),
    ]
