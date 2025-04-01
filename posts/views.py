from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required # 로그인한 사람만 볼 수 있게게

# Create your views here.
def index(request):
    posts = Post.objects.all()
    form = CommentForm()
    context ={
        'posts': posts,
        'form': form,
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

@login_required
def comment_create(request, post_id):
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user # 현재 로그인한 사람
        
        comment.post_id = post_id # id값만 찾아서 게시글몇번인지 추가
        comment.save()
        return redirect('posts:index') 
    
