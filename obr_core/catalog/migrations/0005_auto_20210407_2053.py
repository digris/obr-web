# Generated by Django 3.1.7 on 2021-04-07 18:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0004_auto_20210407_2037"),
    ]

    operations = [
        migrations.AlterField(
            model_name="playlist",
            name="name",
            field=models.CharField(max_length=256, null=True),
        ),
    ]