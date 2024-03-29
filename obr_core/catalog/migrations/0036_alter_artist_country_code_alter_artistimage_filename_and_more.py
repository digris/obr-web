# Generated by Django 4.1.3 on 2023-04-04 06:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0035_auto_20230323_1351"),
    ]

    operations = [
        migrations.AlterField(
            model_name="artist",
            name="country_code",
            field=models.CharField(
                blank=True,
                db_index=True,
                default="",
                max_length=2,
                verbose_name="Country",
            ),
        ),
        migrations.AlterField(
            model_name="artistimage",
            name="filename",
            field=models.CharField(
                default="", editable=False, max_length=512, verbose_name="Filename"
            ),
        ),
        migrations.AlterField(
            model_name="master",
            name="encoding",
            field=models.CharField(db_index=True, default="", max_length=4),
        ),
        migrations.AlterField(
            model_name="mediaartists",
            name="join_phrase",
            field=models.CharField(blank=True, default="", max_length=36),
        ),
        migrations.AlterField(
            model_name="mood",
            name="teaser",
            field=models.CharField(blank=True, default="", max_length=256),
        ),
        migrations.AlterField(
            model_name="mood",
            name="teaser_de",
            field=models.CharField(blank=True, default="", max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name="mood",
            name="teaser_en",
            field=models.CharField(blank=True, default="", max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name="mood",
            name="teaser_fr",
            field=models.CharField(blank=True, default="", max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name="playlist",
            name="name",
            field=models.CharField(default="", max_length=256),
        ),
        migrations.AlterField(
            model_name="playlistimage",
            name="filename",
            field=models.CharField(
                default="", editable=False, max_length=512, verbose_name="Filename"
            ),
        ),
        migrations.AlterField(
            model_name="release",
            name="release_type",
            field=models.CharField(blank=True, default="", max_length=32),
        ),
        migrations.AlterField(
            model_name="releaseimage",
            name="filename",
            field=models.CharField(
                default="", editable=False, max_length=512, verbose_name="Filename"
            ),
        ),
        migrations.AlterField(
            model_name="series",
            name="name",
            field=models.CharField(default="", max_length=256),
        ),
    ]
