# Generated by Django 3.1.8 on 2021-04-17 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0012_release_sync_state"),
    ]

    operations = [
        migrations.AddField(
            model_name="release",
            name="release_date",
            field=models.DateField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="release",
            name="release_type",
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
