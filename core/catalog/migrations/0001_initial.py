# Generated by Django 3.1.7 on 2021-04-01 20:04

import datetime
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Artist",
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
                    "uuid",
                    models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
                ),
                (
                    "uid",
                    models.CharField(
                        db_index=True, editable=False, max_length=8, unique=True
                    ),
                ),
                ("name", models.CharField(max_length=256)),
            ],
            options={
                "verbose_name": "Artist",
                "verbose_name_plural": "Artists",
                "ordering": ["-created"],
            },
        ),
        migrations.CreateModel(
            name="Media",
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
                    "uuid",
                    models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
                ),
                (
                    "uid",
                    models.CharField(
                        db_index=True, editable=False, max_length=8, unique=True
                    ),
                ),
                ("name", models.CharField(max_length=256)),
                ("duration", models.DurationField(default=datetime.timedelta(0))),
            ],
            options={
                "verbose_name": "Media",
                "verbose_name_plural": "Media",
                "ordering": ["-created"],
            },
        ),
        migrations.CreateModel(
            name="MediaArtists",
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
                ("position", models.PositiveSmallIntegerField(default=0)),
                ("join_phrase", models.CharField(blank=True, max_length=36, null=True)),
                (
                    "artist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="media_artist",
                        to="catalog.artist",
                    ),
                ),
                (
                    "media",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="media_artist",
                        to="catalog.media",
                    ),
                ),
            ],
            options={
                "verbose_name": "Media artist",
                "verbose_name_plural": "Media artists",
                "db_table": "catalog_media_artists",
            },
        ),
        migrations.AddField(
            model_name="media",
            name="artists",
            field=models.ManyToManyField(
                blank=True,
                related_name="media",
                through="catalog.MediaArtists",
                to="catalog.Artist",
                verbose_name="Artists",
            ),
        ),
    ]
