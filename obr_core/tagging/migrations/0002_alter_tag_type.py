# Generated by Django 3.2.4 on 2021-09-08 10:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tagging", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tag",
            name="type",
            field=models.CharField(
                choices=[
                    ("genre", "Genre"),
                    ("mood", "Mood"),
                    ("descriptive", "Descriptive"),
                    ("instrument", "Instrument"),
                    ("profession", "Profession"),
                    ("event", "Event"),
                    ("language", "Language"),
                ],
                db_index=True,
                default="genre",
                max_length=16,
            ),
        ),
    ]
