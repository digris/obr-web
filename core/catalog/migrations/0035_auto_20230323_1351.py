# Generated by Django 4.1.3 on 2023-03-23 12:51

from django.contrib.postgres.operations import TrigramExtension, UnaccentExtension
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0034_alter_playlistmedia_options_artistimage_md5_hash_and_more"),
    ]

    operations = [
        UnaccentExtension(),
        TrigramExtension(),
    ]
