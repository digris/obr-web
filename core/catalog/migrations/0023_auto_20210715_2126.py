# Generated by Django 3.2.4 on 2021-07-15 19:26

from django.db import migrations

import tagging.managers


class Migration(migrations.Migration):

    dependencies = [
        ("tagging", "0001_initial"),
        ("catalog", "0022_auto_20210625_1356"),
    ]

    operations = [
        migrations.AlterField(
            model_name="artist",
            name="tags",
            field=tagging.managers.TaggableManager(
                blank=True,
                help_text="A comma-separated list of tags.",
                through="tagging.TaggedItem",
                to="tagging.Tag",
                verbose_name="Tags",
            ),
        ),
        migrations.AlterField(
            model_name="media",
            name="tags",
            field=tagging.managers.TaggableManager(
                blank=True,
                help_text="A comma-separated list of tags.",
                related_name="tagged_media",
                through="tagging.TaggedItem",
                to="tagging.Tag",
                verbose_name="Tags",
            ),
        ),
        migrations.AlterField(
            model_name="playlist",
            name="tags",
            field=tagging.managers.TaggableManager(
                blank=True,
                help_text="A comma-separated list of tags.",
                through="tagging.TaggedItem",
                to="tagging.Tag",
                verbose_name="Tags",
            ),
        ),
        migrations.AlterField(
            model_name="release",
            name="tags",
            field=tagging.managers.TaggableManager(
                blank=True,
                help_text="A comma-separated list of tags.",
                through="tagging.TaggedItem",
                to="tagging.Tag",
                verbose_name="Tags",
            ),
        ),
    ]
