# Generated by Django 3.1.7 on 2021-04-09 21:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0007_auto_20210409_2249"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="media",
            options={
                "ordering": ["name"],
                "verbose_name": "Media",
                "verbose_name_plural": "Media",
            },
        ),
        migrations.AddField(
            model_name="media",
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