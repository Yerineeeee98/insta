from django.forms import ModelForm
from .models import Post, Comment

class PostForm(ModelForm):
    class Meta():
        model = Post
        # fields = '__all__' # user를 선택하지 못하게 
        fields = ('content', 'image')
        
class CommentForm(ModelForm):
    class Meta():
        model = Comment
        fields = ('content', ) # 댓글은 내용만 작성하게