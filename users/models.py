from django.db import models

# Create your models here.
# class User(models.Model):
#     # id = models.IntegerField(primary_key=True, auto_created=True)  -> id 는 자동 생성됨
#     update_date = models.DateTimeField(auto_now_add=True)
#     # auth.User 는 Django 에 자동 생성 되는 User 테이블
#     id_user = models.ForeignKey("auth.User", related_name="config_user", on_delete=models.CASCADE, db_column="id_user")


# # 20231127 프로필 화면을 위한 코드
# from django.contrib.auth.models import User
# from django.db import models
# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# # 추가 정보를 저장할 Profile 모델 생성
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     nickname = models.CharField(max_length=50, blank=True)  # 닉네임
#     age = models.IntegerField(blank=True, null=True)  # 나이 등 원하는 추가 정보 필드들을 정의합니다.
#
#     # 추가 정보를 출력하는 방법을 설정할 수 있습니다.
#     def __str__(self):
#         return f'{self.user.username}의 프로필'
#
# @receiver(post_save, sender=User)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#     if created or not hasattr(instance, 'profile'):
#         Profile.objects.create(user=instance)
#     else:
#         instance.profile.save()

# 20231128 프로필을 위한 모델
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_images', blank=True, null=True)
    # 추가적인 프로필 필드들을 여기에 추가할 수 있습니다.
