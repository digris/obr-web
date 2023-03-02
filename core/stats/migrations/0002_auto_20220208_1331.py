# Generated by Django 3.2.10 on 2022-02-08 12:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stats", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="playerevent",
            options={"ordering": ["time"], "verbose_name": "Player event"},
        ),
        migrations.AddField(
            model_name="playerevent",
            name="ingested",
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]
