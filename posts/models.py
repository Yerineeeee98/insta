from django.db import models
from django_resized import ResizedImageField
from django.conf import settings

# Create your models here.
class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # image = models.ImageField(upload_to='image')
    image = ResizedImageField(
        size=[500, 500], 
        crop=['middle', 'center'],
        upload_to='image/%Y/%m'
    )
    # 작성자
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # 게시물을 좋아요 누른 사람들, m : n으로 연결하고싶음
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name = 'like_posts', # 작성자와 게시물을 좋아요 누른 사람들 사이에 역참조가 충돌해서 새로 설정하기 
        ) 
    
    
class Comment(models.Model):
    content = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    