# Generated by Django 4.1.3 on 2023-03-30 14:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stats", "0006_alter_streamevent_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="streamevent",
            name="bytes_sent",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="streamevent",
            name="seconds_connected",
            field=models.PositiveIntegerField(
                db_index=True, default=0, verbose_name="duration"
            ),
        ),
    ]
