from django.forms import ModelForm
from .models import Post

class PostForm(ModelForm):
    class Meta():
        model = Post
        # fields = '__all__' # user를 선택하지 못하게 
        fields = ('content', 'image')