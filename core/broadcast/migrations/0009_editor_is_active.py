# Generated by Django 3.2.10 on 2022-03-07 16:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("broadcast", "0008_editor_role"),
    ]

    operations = [
        migrations.AddField(
            model_name="editor",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
