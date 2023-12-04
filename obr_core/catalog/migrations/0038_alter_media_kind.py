# Generated by Django 4.2.7 on 2023-12-04 11:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0037_alter_artistimage_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="media",
            name="kind",
            field=models.CharField(
                blank=True,
                choices=[
                    ("", "Not specified"),
                    ("song", "Song"),
                    ("acappella", "A cappella"),
                    ("soundeffects", "Sound effects"),
                    ("soundtrack", "Soundtrack"),
                    ("spokenword", "Spokenword"),
                    ("interview", "Interview"),
                    ("jingle", "Jingle"),
                    ("djmix", "DJ-Mix"),
                    ("concert", "Concert"),
                    ("liveact", "Live Act PA)"),
                    ("radioshow", "Radio show"),
                ],
                db_index=True,
                default="",
                max_length=16,
                null=True,
            ),
        ),
    ]