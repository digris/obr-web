# Generated by Django 5.0.7 on 2025-06-07 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("donation", "0002_donation_price_id_donation_subscription_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="donation",
            old_name="extra_data",
            new_name="payment_intent_data",
        ),
        migrations.AddField(
            model_name="donation",
            name="kind",
            field=models.CharField(
                choices=[("single", "Single"), ("recurring", "Recurring")],
                db_index=True,
                default="single",
                max_length=16,
                verbose_name="Kind",
            ),
        ),
        migrations.AddField(
            model_name="donation",
            name="subscription_data",
            field=models.JSONField(
                blank=True, default=dict, help_text="only used for recurring donations"
            ),
        ),
        migrations.AlterField(
            model_name="donation",
            name="price_id",
            field=models.CharField(
                blank=True,
                db_index=True,
                default="",
                help_text="only used for recurring donations",
                max_length=256,
                verbose_name="Stripe price",
            ),
        ),
        migrations.AlterField(
            model_name="donation",
            name="state",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("succeeded", "Succeeded"),
                    ("failed", "Failed"),
                ],
                db_index=True,
                default="pending",
                max_length=16,
                verbose_name="State",
            ),
        ),
        migrations.AlterField(
            model_name="donation",
            name="subscription_id",
            field=models.CharField(
                blank=True,
                db_index=True,
                default="",
                help_text="only used for recurring donations",
                max_length=256,
                verbose_name="Stripe subscription",
            ),
        ),
        migrations.AlterField(
            model_name="donation",
            name="user_identity",
            field=models.CharField(
                blank=True,
                db_index=True,
                default="",
                help_text="only used for single donations (anonymous users)",
                max_length=64,
            ),
        ),
    ]
