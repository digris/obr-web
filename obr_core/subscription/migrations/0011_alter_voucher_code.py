# Generated by Django 3.2.16 on 2022-11-24 22:29

from django.db import migrations, models

import subscription.models.voucher


class Migration(migrations.Migration):
    dependencies = [
        ("subscription", "0010_subscription_countries_str"),
    ]

    operations = [
        migrations.AlterField(
            model_name="voucher",
            name="code",
            field=models.CharField(
                db_index=True,
                default=subscription.models.voucher.get_default_code,
                max_length=6,
                unique=True,
            ),
        ),
    ]
