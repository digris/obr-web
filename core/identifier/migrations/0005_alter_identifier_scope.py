# Generated by Django 3.2.16 on 2022-11-24 22:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("identifier", "0004_alter_identifier_scope"),
    ]

    operations = [
        migrations.AlterField(
            model_name="identifier",
            name="scope",
            field=models.CharField(
                choices=[
                    ("musicbrainz", "Musicbrainz"),
                    ("obp", "open broadcast platform"),
                    ("discogs", "Discogs"),
                    ("wikipedia", "Wikipedia"),
                    ("soundcloud", "SoundCloud"),
                    ("official", "Website"),
                    ("isrc", "ISRC"),
                ],
                db_index=True,
                max_length=32,
                null=True,
            ),
        ),
    ]
