# Generated by Django 5.0.7 on 2025-02-24 18:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0039_label_labelimage"),
    ]

    operations = [
        migrations.AddField(
            model_name="release",
            name="label",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="releases",
                to="catalog.label",
            ),
        ),
    ]
