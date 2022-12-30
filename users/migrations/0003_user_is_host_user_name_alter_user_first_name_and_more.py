# Generated by Django 4.1.3 on 2022-12-30 10:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_remove_user_is_host_remove_user_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_host",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="user",
            name="name",
            field=models.CharField(default="", max_length=150),
        ),
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(editable=False, max_length=150),
        ),
        migrations.AlterField(
            model_name="user",
            name="last_name",
            field=models.CharField(editable=False, max_length=150),
        ),
    ]
