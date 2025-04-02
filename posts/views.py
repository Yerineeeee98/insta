from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required # 로그인한 사람만 볼 수 있게게
from django.http import JsonResponse

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
        
        comment.post_id = post_id # 이 댓글이 어느 게시글에 달리는지 표시해주는 정보
        comment.save()
        return redirect('posts:index') 
@login_required    
def like(request, post_id):
    user = request.user # 현재 로그인한 사람
    post = Post.objects.get(id = post_id)
    
    # if post in user.like_posts.all(): # 유저가 좋아요 누른 게시물에 포스터가 있나요 모델에서 가져옴 
    # 밑에 코드와 똑같은 기능을 가짐     
    
    if user in post.like_users.all(): # 이 게시물에 좋아요 버튼 누른 사람들의 목록에 그 사람이 있나
        # user.like_posts.remove(post)
        post.like_users.remove(user) # 좋아요를 이미 눌렀다면 지워주기
    else:
        # user.like_posts.add(post)
        post.like_users.add(user) # user 추가
        
    return redirect('posts:index')

def feed(request):
    followings = request.user.followings.all()
    
    posts = Post.objects.filter(user__in=followings) # 내가 팔로우 하는 사람들이 작성한 게시물들 
    form = CommentForm()
    
    context = {
        'posts':posts,
        'form':form,
    }
    
    return render(request, 'index.html', context)

def like_async(request, id):
    user = request.user
    post = Post.objects.get(id = id)
    
    if user in post.like_users.all():
        post.like_users.remove(user)
        status = False
    else:
        post.like_users.add(user)
        status = True
    context = {
        'post_id': id, 
        'status': status,
        'count': len(post.like_users.all())
    }
    return JsonResponse(context)