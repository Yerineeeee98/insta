from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required # 로그인한 사람만 볼 수 있게게

# Create your views here.
def index(request):
    posts = Post.objects.all()

    context ={
        'posts': posts,
    }

    return render(request, 'index.html', context)

@login_required # 로그인한 사람만 게시물을 작성할수있게
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit = False) # user정보가 빠져있음
            post.user = request.user
            post.save()
            return redirect('posts:index')
    else:
        form = PostForm()

    context = {
        'form': form,
    }
    return render(request, 'create.html', context)
