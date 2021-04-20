# Generated by Django 3.1.8 on 2021-04-14 18:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0010_auto_20210414_1550"),
    ]

    operations = [
        migrations.AddField(
            model_name="playlistmedia",
            name="uid",
            field=models.CharField(
                db_index=True, editable=False, max_length=8, null=True, unique=True
            ),
        ),
        migrations.AddField(
            model_name="playlistmedia",
            name="uuid",
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
        ),
    ]
