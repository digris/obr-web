# Generated by Django 3.2.13 on 2022-05-18 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0031_mood_style"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mood",
            name="style",
            field=models.JSONField(default=dict),
        ),
    ]
