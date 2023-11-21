# Generated by Django 4.1.3 on 2023-04-04 06:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("subscription", "0014_voucher_inherit"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="transaction_id",
            field=models.CharField(
                blank=True,
                db_index=True,
                default="",
                max_length=256,
                verbose_name="Transaction ID",
            ),
        ),
    ]