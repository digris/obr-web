# Generated by Django 4.1.3 on 2023-01-27 18:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0033_auto_20220608_1906"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="playlistmedia",
            options={
                "ordering": ["position"],
                "verbose_name": "Playlist media",
                "verbose_name_plural": "Playlist media",
            },
        ),
        migrations.AddField(
            model_name="artistimage",
            name="md5_hash",
            field=models.CharField(default="", max_length=32),
        ),
        migrations.AddField(
            model_name="playlistimage",
            name="md5_hash",
            field=models.CharField(default="", max_length=32),
        ),
        migrations.AddField(
            model_name="releaseimage",
            name="md5_hash",
            field=models.CharField(default="", max_length=32),
        ),
    ]
