# Generated by Django 3.2.16 on 2022-11-24 22:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tagging", "0003_tag_sync_last_update"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tag",
            name="slug",
            field=models.SlugField(
                allow_unicode=True, max_length=100, unique=True, verbose_name="slug"
            ),
        ),
    ]
