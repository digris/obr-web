# Generated by Django 3.1.8 on 2021-04-17 13:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0011_auto_20210414_2005"),
    ]

    operations = [
        migrations.AddField(
            model_name="release",
            name="sync_state",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("running", "Running"),
                    ("completed", "Completed"),
                    ("failed", "Failed"),
                ],
                db_index=True,
                default="pending",
                max_length=16,
            ),
        ),
    ]
