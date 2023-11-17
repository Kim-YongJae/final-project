from django.shortcuts import render

# Create your views here.
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.contrib.auth.decorators import login_required
from .forms import PostForm  # PostForm은 게시물 생성을 위한 폼입니다.

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'services/post_list.html', {'posts': posts})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'services/post_detail.html', {'post': post})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            # 현재 로그인한 사용자를 작성자로 지정하여 새로운 게시물 생성
            new_post = Post(title=title, content=content, author=request.user)
            new_post.save()
            return redirect('post_detail', pk=new_post.pk)  # 생성된 게시물 상세 페이지로 이동
    else:
        form = PostForm()  # GET 요청 시 빈 폼을 생성하여 사용자에게 제공

    return render(request, 'services/post_create.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()  # 폼 데이터를 저장하여 게시물을 업데이트합니다.
            return redirect('post_detail', pk=pk)  # 수정된 게시물 상세 페이지로 이동
    else:
        form = PostForm(instance=post)  # 기존 게시물 데이터를 폼에 채워서 사용자에게 제공

    return render(request, 'services/post_edit.html', {'form': form, 'post': post})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()  # 게시물 삭제
        return redirect('post_list')  # 삭제 후 목록 페이지로 이동

    return render(request, 'services/post_delete.html', {'post': post})