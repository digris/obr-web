# Generated by Django 4.1.3 on 2023-04-04 06:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rating", "0010_vote_uid_vote_uuid"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="vote",
            options={
                "ordering": ["-updated"],
                "verbose_name": "Vote",
                "verbose_name_plural": "Votes",
            },
        ),
        migrations.AlterField(
            model_name="vote",
            name="scope",
            field=models.CharField(
                choices=[
                    ("", "not specified"),
                    ("track", "track"),
                    ("emission", "emission"),
                    ("daytime", "daytime"),
                    ("repetition", "repetition"),
                    ("genre", "genre"),
                ],
                db_index=True,
                default="",
                max_length=16,
            ),
        ),
        migrations.AlterField(
            model_name="vote",
            name="user_identity",
            field=models.CharField(
                blank=True, db_index=True, default="", max_length=64
            ),
        ),
    ]
