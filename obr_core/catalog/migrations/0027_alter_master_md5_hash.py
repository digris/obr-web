# Generated by Django 3.2.7 on 2021-12-08 14:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0026_auto_20211117_1350"),
    ]

    operations = [
        migrations.AlterField(
            model_name="master",
            name="md5_hash",
            field=models.CharField(default="", max_length=32),
        ),
    ]
