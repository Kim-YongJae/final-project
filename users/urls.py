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
from django.contrib import admin
from django.urls import path
from users import views

urlpatterns = [
    path("", views.index, name="index"),
    path('search_id/', views.search_id, name='search_id'),
    path('find_password/', views.find_password, name='find_password'),
    path("register/", views.register, name="register"),
    path("login/", views.sign_in, name="login"),
    path('logout/', views.user_logout, name='logout'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path("Information_Modification/", views.Information_Modification, name="Information_Modification"),
    path("Withdrawal/", views.Withdrawal, name="Withdrawal"),
    path("profile_edit/", views.profile_edit_view, name="profile_edit"),
    path('profile_password/', views.password_edit_view, name='profile_password'),

]

