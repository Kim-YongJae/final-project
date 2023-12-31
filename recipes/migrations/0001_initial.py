# Generated by Django 4.2.7 on 2023-11-27 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Recipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("food_name", models.CharField(max_length=255)),
                ("ingredients", models.TextField()),
                ("recipe_steps", models.TextField()),
                ("label", models.CharField(max_length=255)),
            ],
        ),
    ]
