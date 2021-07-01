# Generated by Django 3.2.4 on 2021-06-24 07:39

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0007_logintoken"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="sync_last_update",
            field=models.DateTimeField(
                db_index=True, default=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=utc)
            ),
        ),
    ]
