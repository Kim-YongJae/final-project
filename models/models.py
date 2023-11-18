from django.db import models

# Create your models here.
class Model(models.Model):
    # id = models.IntegerField(primary_key=True, auto_created=True)  -> id 는 자동 생성됨
    # food_photo = models.ImageField(upload_to='recipes/recipe_photos/', null=True, blank=True)
    Photo_label = models.CharField(max_length=255)