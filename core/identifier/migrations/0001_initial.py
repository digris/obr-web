# Generated by Django 3.2 on 2021-06-03 09:19

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Identifier",
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
                (
                    "scope",
                    models.CharField(
                        choices=[
                            ("generic", "Generic"),
                            ("musicbrainz", "Musicbrainz"),
                            ("obp", "open broadcast platform"),
                        ],
                        db_index=True,
                        max_length=32,
                    ),
                ),
                (
                    "value",
                    models.CharField(
                        db_index=True, max_length=256, verbose_name="Identifier"
                    ),
                ),
                ("object_id", models.PositiveIntegerField()),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={
                "verbose_name": "Identifier",
                "verbose_name_plural": "Identifiers",
                "unique_together": {("scope", "value", "content_type", "object_id")},
            },
        ),
    ]
