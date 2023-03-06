# Generated by Django 3.2.15 on 2022-10-03 17:56

from django.db import migrations, models


def gender_int_to_str(apps, schema_editor):
    User = apps.get_model("account", "User")
    db_alias = schema_editor.connection.alias
    base_qs = User.objects.using(db_alias)
    base_qs.filter(gender=0,).update(
        gender_str="",
    )
    base_qs.filter(gender=1,).update(
        gender_str="female",
    )
    base_qs.filter(gender=2,).update(
        gender_str="male",
    )
    base_qs.filter(gender=3,).update(
        gender_str="other",
    )


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0018_auto_20220608_1933"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="gender_str",
            field=models.CharField(
                choices=[
                    ("", "undefined"),
                    ("female", "female"),
                    ("male", "male"),
                    ("other", "other"),
                ],
                default="",
                max_length=16,
            ),
        ),
        migrations.RunPython(gender_int_to_str),
    ]
