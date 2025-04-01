from django.db import models
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField

# Create your models here.

class User(AbstractUser):
    profile_image = ResizedImageField(
        size=[500, 500], 
        crop=['middle', 'center'],
        upload_to='image/%Y/%m'
    )
    followings = models.ManyToManyField('self', related_name = 'followers', symmetrical=False) # 내가 팔로우한 사람 m:n # self는 나 스스로를 m:n으로 연결
    # symmetrical 대칭적인가 false를 줌으로써 단방향을 의미 