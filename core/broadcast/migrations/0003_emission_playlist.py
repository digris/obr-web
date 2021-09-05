# Generated by Django 3.1.7 on 2021-04-07 18:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0004_auto_20210407_2037"),
        ("broadcast", "0002_auto_20210407_2023"),
    ]

    operations = [
        migrations.AddField(
            model_name="emission",
            name="playlist",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="catalog.playlist",
            ),
        ),
    ]
