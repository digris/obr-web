# Generated by Django 5.0.7 on 2024-12-02 08:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("qr_redirect", "0003_qrredirect_name_alter_qrredirect_target_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="qrredirect",
            name="qr_code",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="get_qr_code_upload_path",
                verbose_name="QR-Code",
            ),
        ),
    ]
