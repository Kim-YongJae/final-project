from django.db import models
from django.contrib.auth.models import User
import json

# Create your models here.
class Recipe(models.Model):
    # id = models.IntegerField(primary_key=True, auto_created=True)  -> id 는 자동 생성됨
    # food_photo = models.ImageField(upload_to='recipes/recipe_photos/', null=True, blank=True)

    food_name = models.CharField(max_length=255)
    ingredients = models.TextField()
    recipe_steps = models.TextField()
    label = models.JSONField(default=list)
    food_photo = models.ImageField(upload_to='recipes/recipe_photos/', null=True, blank=True)
    # 새로운 필드: 레시피 평점 및 평가 횟수
    rating = models.FloatField(default=0.0)  # 기본값은 0.0으로 설정해둠
    rating_count = models.PositiveIntegerField(default=0)

    # ArrayField(models.IntegerField()) sqlite에서 지원하지 않음 json.loads()를 통해서 리스트형태로 변환가능[]
class favorite(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ffood_name = models.CharField(max_length=255)
    fingredients = models.TextField()
    frecipe_steps = models.TextField()
    # def __str__(self):
    #     return self.food_name