# Generated by Django 5.0.7 on 2025-05-19 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0044_label_root_alter_label_kind"),
    ]

    operations = [
        migrations.AddField(
            model_name="media",
            name="lyrics_explicit",
            field=models.IntegerField(
                choices=[(0, "Clean"), (1, "Explicit")], default=0
            ),
        ),
        migrations.AddField(
            model_name="media",
            name="lyrics_language",
            field=models.CharField(blank=True, default="", max_length=5),
        ),
        migrations.AddField(
            model_name="media",
            name="lyrics_text",
            field=models.TextField(blank=True, default=""),
        ),
    ]
