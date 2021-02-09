from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Post, Group
from .forms import PostForm

User = get_user_model()


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "index.html", {"page": page, "paginator": paginator})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "group.html", {"group": group, "page": page, "paginator": paginator})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "profile.html", {"author": user,
                                            "page": page, "paginator": paginator})


def post_view(request, username, post_id):
    user = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, id=post_id, author=user)
    return render(request, "post.html", {"author": user,
                                         "post": post})


def post_edit(request, username, post_id):
    if request.user.username != username:
        return redirect("post", username=username, post_id=post_id)
    post = get_object_or_404(Post, id=post_id, author__username=username)
    if request.method == "POST":
        form = PostForm(request.POST or None, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post", username=username, post_id=post_id)
    form = PostForm(instance=post)
    return render(request, "new.html", {"username": username,
                                        "post": post, "form": form})


@login_required
def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            return redirect("index")
    form = PostForm()
    return render(request, "new.html", {"form": form})
