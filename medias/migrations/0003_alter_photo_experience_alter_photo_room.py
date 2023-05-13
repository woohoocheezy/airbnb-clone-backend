# Generated by Django 4.1.3 on 2023-05-13 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        (
            "experiences",
            "0003_alter_experience_category_alter_experience_host_and_more",
        ),
        ("rooms", "0005_alter_room_amenities_alter_room_category_and_more"),
        ("medias", "0002_alter_photo_experience_alter_photo_file_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="photo",
            name="experience",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="photos",
                to="experiences.experience",
            ),
        ),
        migrations.AlterField(
            model_name="photo",
            name="room",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="photos",
                to="rooms.room",
            ),
        ),
    ]