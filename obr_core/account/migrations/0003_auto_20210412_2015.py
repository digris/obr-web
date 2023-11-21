# Generated by Django 3.1.7 on 2021-04-12 18:15

from uuid import uuid4

from django.conf import settings
from django.db import migrations, models


def forwards_func(apps, schema_editor):
    if getattr(settings, "TEST_MODE", False):
        print("TEST_MODE detected - skipping migration")
        return

    User = apps.get_model("account", "User")
    db_alias = schema_editor.connection.alias
    for user in User.objects.using(db_alias).all():
        uuid = uuid4()
        uid = str(uuid)[:8].upper()
        user.uuid = uuid
        user.uid = uid
        user.save()
        # User.objects.filter(id=user.id).update(uid=user.get_uid())


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0002_create_superuser"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
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
        migrations.AddField(
            model_name="user",
            name="uid",
            field=models.CharField(
                db_index=True, editable=False, max_length=8, null=True, unique=True
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="uuid",
            field=models.UUIDField(db_index=True, default=uuid4, editable=False),
        ),
        migrations.RunPython(forwards_func, reverse_func),
    ]