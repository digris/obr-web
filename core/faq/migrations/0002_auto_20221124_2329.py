# Generated by Django 3.2.16 on 2022-11-24 22:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("faq", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={
                "ordering": ["-priority", "name"],
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.AlterField(
            model_name="topic",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="topics",
                to="faq.category",
            ),
        ),
    ]
