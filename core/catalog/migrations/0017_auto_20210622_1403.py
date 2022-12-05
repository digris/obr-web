# Generated by Django 3.2.4 on 2021-06-22 12:03

from django.db import migrations, models

import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ("tagging", "0001_initial"),
        ("catalog", "0016_auto_20210601_1835"),
    ]

    operations = [
        migrations.AddField(
            model_name="artist",
            name="country_code",
            field=models.CharField(
                blank=True,
                db_index=True,
                max_length=2,
                null=True,
                verbose_name="Country",
            ),
        ),
        migrations.AddField(
            model_name="artist",
            name="date_end",
            field=models.DateField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="artist",
            name="date_start",
            field=models.DateField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="artist",
            name="tags",
            field=taggit.managers.TaggableManager(
                blank=True,
                help_text="A comma-separated list of tags.",
                through="tagging.TaggedItem",
                to="tagging.Tag",
                verbose_name="Tags",
            ),
        ),
    ]
