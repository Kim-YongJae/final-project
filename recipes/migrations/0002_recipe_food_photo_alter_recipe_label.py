# Generated by Django 4.2.7 on 2023-11-30 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="recipe",
            name="food_photo",
            field=models.ImageField(
                blank=True, null=True, upload_to="recipes/recipe_photos/"
            ),
        ),
        migrations.AlterField(
            model_name="recipe", name="label", field=models.JSONField(default=list),
        ),
    ]
