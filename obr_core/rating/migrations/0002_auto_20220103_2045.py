# Generated by Django 3.2.10 on 2022-01-03 19:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rating", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="vote",
            name="comment",
            field=models.TextField(default="", max_length=256),
        ),
        migrations.AddField(
            model_name="vote",
            name="scope",
            field=models.CharField(
                choices=[
                    ("None", "not classified"),
                    ("track", "track"),
                    ("emission", "emission"),
                    ("daytime", "daytime"),
                    ("repetition", "repetition"),
                ],
                db_index=True,
                default="None",
                max_length=16,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="vote",
            name="value",
            field=models.SmallIntegerField(
                choices=[(-1, "-"), (1, "+")], db_index=True
            ),
        ),
    ]
