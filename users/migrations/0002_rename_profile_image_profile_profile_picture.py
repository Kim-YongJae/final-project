# Generated by Django 4.2.7 on 2023-11-28 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="profile", old_name="profile_image", new_name="profile_picture",
        ),
    ]