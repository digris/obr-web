# Generated by Django 4.2.7 on 2024-06-26 08:26

from django.db import migrations, models

import django_countries.fields


class Migration(migrations.Migration):
    dependencies = [
        ("stats", "0013_streamevent_geoip_city_streamevent_geoip_country_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="streamevent",
            name="geoip_city",
            field=models.CharField(
                blank=True, db_index=True, default="", max_length=128
            ),
        ),
        migrations.AlterField(
            model_name="streamevent",
            name="geoip_country",
            field=django_countries.fields.CountryField(
                blank=True, db_index=True, default="", max_length=2
            ),
        ),
        migrations.AlterField(
            model_name="streamevent",
            name="geoip_region",
            field=models.CharField(
                blank=True, db_index=True, default="", max_length=128
            ),
        ),
    ]
