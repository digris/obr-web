# Generated by Django 3.2.15 on 2022-10-03 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0020_rename_gender_user_gender_int"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="gender_str",
            new_name="gender",
        ),
    ]
