# Generated by Django 3.1.7 on 2021-03-25 11:03

import google.auth
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import migrations

try:
    from google.cloud import secretmanager as sm
except ImportError as e:
    print("unable to import secretmanager")
    sm = None


def create_superuser(apps, schema_editor):
    if getattr(settings, "TEST_MODE", False):
        print("TEST_MODE detected - skipping migration")
        return
    if not sm:
        return
    # superuser secret as <email>:<password>
    # to create secret:
    # gcloud secrets create ch-openbroadcast-superuser --replication-policy automatic
    # echo -n "foo@bar.baz:correcthorsebatterystaple" | gcloud secrets versions add ch-openbroadcast-superuser --data-file=-
    _, project = google.auth.default()
    client = sm.SecretManagerServiceClient()
    name = f"projects/{project}/secrets/ch-openbroadcast-superuser/versions/latest"
    superuser = client.access_secret_version(name=name).payload.data.decode("UTF-8")
    email, password = superuser.split(":")
    get_user_model().objects.create_superuser(email=email, password=password)


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        # migrations.RunPython(create_superuser),
    ]
