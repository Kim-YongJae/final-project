# Create your views here.
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.contrib.auth.decorators import login_required
from .forms import PostForm  # PostForm은 게시물 생성을 위한 폼입니다.
from django.http import HttpResponseNotAllowed, HttpResponseForbidden, HttpResponse
from django.utils.safestring import mark_safe
from django.core.paginator import Paginator


def post_list(request):
    all_posts = Post.objects.order_by('-created_at')
    paginator = Paginator(all_posts, 10)  # 페이지당 10개의 포스트를 보여줌

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for post in page_obj:
        post.views = post.views  # 조회수 필드 가져오기
        post.save()  # 변경사항 저장

    return render(request, 'services/post_list.html', {'page_obj': page_obj})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.content = mark_safe(post.content) # content를 안전한 HTML로 표시
    post.increase_views()  # 조회수 증가 메서드 호출
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
    # 작성자 확인
    if post.author != request.user:
        return redirect('post_detail', pk=pk)  # 혹은 원하는 경로로 리다이렉트

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

    if post.author != request.user:
        return redirect('post_detail', pk=pk)  # 혹은 원하는 경로로 리다이렉트

    if request.method == 'POST':
        post.delete()  # 게시물 삭제
        return redirect('post_list')  # 삭제 후 목록 페이지로 이동
    else:
        return HttpResponseNotAllowed(['POST'])  # POST 요청 외에는 허용하지 않음

def check_permission(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden()  # 권한이 없는 경우 403 Forbidden 반환
    else:
        return HttpResponse()  # 권한이 있는 경우 아무 작업 없이 200 OK 반환