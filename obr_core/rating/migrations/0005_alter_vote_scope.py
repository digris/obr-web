# Generated by Django 3.2.10 on 2022-03-11 18:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rating", "0004_alter_vote_scope"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vote",
            name="scope",
            field=models.CharField(
                choices=[
                    ("None", "not specified"),
                    ("track", "track"),
                    ("emission", "emission"),
                    ("daytime", "daytime"),
                    ("repetition", "repetition"),
                    ("genre", "genre"),
                ],
                db_index=True,
                default="None",
                max_length=16,
                null=True,
            ),
        ),
    ]