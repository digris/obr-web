# Generated by Django 3.2 on 2021-05-20 16:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("subscription", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscription",
            name="type",
            field=models.CharField(
                choices=[("plan", "Plan"), ("trial", "Trial")],
                db_index=True,
                default="plan",
                max_length=16,
            ),
        ),
    ]
