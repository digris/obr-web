# Generated by Django 5.0.7 on 2024-12-02 09:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("qr_redirect", "0004_qrredirect_qr_code"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="qrredirect",
            name="qr_code",
        ),
        migrations.AddField(
            model_name="qrredirect",
            name="num_clicks",
            field=models.PositiveIntegerField(
                default=0, verbose_name="Number of Clicks"
            ),
        ),
    ]