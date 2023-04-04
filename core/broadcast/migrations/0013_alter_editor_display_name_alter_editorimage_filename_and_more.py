# Generated by Django 4.1.3 on 2023-04-04 06:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("broadcast", "0012_editorimage_md5_hash"),
    ]

    operations = [
        migrations.AlterField(
            model_name="editor",
            name="display_name",
            field=models.CharField(
                blank=True, default="", max_length=256, verbose_name="Display name"
            ),
        ),
        migrations.AlterField(
            model_name="editorimage",
            name="filename",
            field=models.CharField(
                default="", editable=False, max_length=512, verbose_name="Filename"
            ),
        ),
        migrations.AlterField(
            model_name="emission",
            name="obj_key",
            field=models.CharField(default="", editable=False, max_length=128),
        ),
    ]
