"""
URL configuration for Ingredient_Detecting project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from recipes import views
from recipes.views import RecipeList, RecipeDetail

urlpatterns = [
    path('recipes/', RecipeList.as_view(), name='recipe_list'),
    path('recipes/<int:recipe_id>/', RecipeDetail.as_view(), name='recipe_detail'),
    path('recipes/recommend/', views.detect_ingredients, name='detect_ingredients'),
]
