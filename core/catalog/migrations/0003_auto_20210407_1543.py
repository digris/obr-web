# Generated by Django 3.1.7 on 2021-04-07 13:43

import uuid

import django.db.models.deletion
from django.db import migrations, models

import image.models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0002_artistimage"),
    ]

    operations = [
        migrations.CreateModel(
            name="Release",
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
                "verbose_name": "Release",
                "verbose_name_plural": "Releases",
                "ordering": ["-created"],
            },
        ),
        migrations.CreateModel(
            name="ReleaseMedia",
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
                (
                    "media",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="release_media",
                        to="catalog.media",
                    ),
                ),
                (
                    "release",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="release_media",
                        to="catalog.release",
                    ),
                ),
            ],
            options={
                "verbose_name": "Release media",
                "verbose_name_plural": "Release media",
                "db_table": "catalog_release_media",
            },
        ),
        migrations.CreateModel(
            name="ReleaseImage",
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
                (
                    "file",
                    models.ImageField(
                        null=True,
                        upload_to=image.models.get_image_upload_path,
                        verbose_name="File",
                    ),
                ),
                (
                    "filename",
                    models.CharField(
                        editable=False,
                        max_length=512,
                        null=True,
                        verbose_name="Filename",
                    ),
                ),
                (
                    "position",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, 1),
                            (2, 2),
                            (3, 3),
                            (4, 4),
                            (5, 5),
                            (6, 6),
                            (7, 7),
                            (8, 8),
                            (9, 9),
                            (10, 10),
                            (11, 11),
                            (12, 12),
                            (13, 13),
                            (14, 14),
                            (15, 15),
                            (16, 16),
                            (17, 17),
                            (18, 18),
                            (19, 19),
                            (20, 20),
                            (21, 21),
                            (22, 22),
                            (23, 23),
                            (24, 24),
                            (25, 25),
                            (26, 26),
                            (27, 27),
                            (28, 28),
                            (29, 29),
                            (30, 30),
                            (31, 31),
                            (32, 32),
                            (33, 33),
                            (34, 34),
                            (35, 35),
                            (36, 36),
                            (37, 37),
                            (38, 38),
                            (39, 39),
                            (40, 40),
                            (41, 41),
                            (42, 42),
                            (43, 43),
                            (44, 44),
                            (45, 45),
                            (46, 46),
                            (47, 47),
                            (48, 48),
                            (49, 49),
                            (50, 50),
                            (51, 51),
                            (52, 52),
                            (53, 53),
                            (54, 54),
                            (55, 55),
                            (56, 56),
                            (57, 57),
                            (58, 58),
                            (59, 59),
                            (60, 60),
                            (61, 61),
                            (62, 62),
                            (63, 63),
                            (64, 64),
                            (65, 65),
                            (66, 66),
                            (67, 67),
                            (68, 68),
                            (69, 69),
                            (70, 70),
                            (71, 71),
                            (72, 72),
                            (73, 73),
                            (74, 74),
                            (75, 75),
                            (76, 76),
                            (77, 77),
                            (78, 78),
                            (79, 79),
                            (80, 80),
                            (81, 81),
                            (82, 82),
                            (83, 83),
                            (84, 84),
                            (85, 85),
                            (86, 86),
                            (87, 87),
                            (88, 88),
                            (89, 89),
                            (90, 90),
                            (91, 91),
                            (92, 92),
                            (93, 93),
                            (94, 94),
                            (95, 95),
                            (96, 96),
                            (97, 97),
                            (98, 98),
                            (99, 99),
                        ],
                        default=1,
                        verbose_name="Position",
                    ),
                ),
                (
                    "release",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="catalog.release",
                    ),
                ),
            ],
            options={
                "verbose_name": "Image",
                "verbose_name_plural": "Images",
                "ordering": ["position"],
            },
        ),
        migrations.AddField(
            model_name="release",
            name="media",
            field=models.ManyToManyField(
                blank=True,
                related_name="releases",
                through="catalog.ReleaseMedia",
                to="catalog.Media",
                verbose_name="Artists",
            ),
        ),
    ]
