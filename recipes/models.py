from django.db import models

# Create your models here.
class Recipe(models.Model):
    # id = modelz.IntegerField(primary_key=True, auto_created=True)  -> id 는 자동 생성됨
    # food_photo = modelz.ImageField(upload_to='recipes/recipe_photos/', null=True, blank=True)
    food_name = models.CharField(max_length=255)
    ingredients = models.TextField()
    recipe_steps = models.TextField()
    label = models.CharField(max_length=255)

    # ArrayField(modelz.IntegerField()) sqlite에서 지원하지 않음 json.loads()를 통해서 리스트형태로 변환가능[]
    # def __str__(self):
    #     return self.food_name