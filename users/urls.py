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
# 20231128 프로필 사진때문에 추가?
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.recipe_random_list, name="index"),
    path('search_id/', views.search_id, name='search_id'),
    path('find_password/', views.find_password, name='find_password'), # 20231128 변경
    #path('find_password/', views.reset_password, name='find_password'), #20231124 변경
    #path('reset_password/', views.reset_password, name='reset_password'),  # reset_password 뷰에 대한 URL 추가 20231124
    path("register/", views.register, name="register"),
    path("login/", views.sign_in, name="login"),
    path('logout/', views.user_logout, name='logout'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path("Information_Modification/", views.Information_Modification, name="Information_Modification"),
    path("Withdrawal/", views.Withdrawal, name="Withdrawal"),
    path("profile_edit/", views.profile_edit_view, name="profile_edit"),
    path('profile_password/', views.password_edit_view, name='profile_password'),
    path('upload_profile_picture/', views.upload_profile_picture, name='upload_profile_picture'), # 20231128 프로필 메인화면 추가
]

# 20231128 프로필 사진때문에 추가?
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)