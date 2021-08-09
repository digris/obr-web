# Generated by Django 3.2.4 on 2021-07-15 19:27

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0023_auto_20210715_2126"),
    ]

    operations = [
        migrations.CreateModel(
            name="Mood",
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
                        db_index=True,
                        editable=False,
                        max_length=8,
                        null=True,
                        unique=True,
                    ),
                ),
                ("name", models.CharField(max_length=36)),
                ("teaser", models.CharField(blank=True, max_length=256, null=True)),
            ],
            options={
                "verbose_name": "Mood",
                "verbose_name_plural": "Moods",
                "ordering": ["name"],
            },
        ),
    ]
