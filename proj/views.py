from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from proj.models import Post


def index_view(request):

    posts = Post.objects.all().order_by("-id")

    for post in posts:
        post.username = post.author.get_username()

    context = {"posts": posts}

    return render(request, "index.html", context)


@require_http_methods(["GET", "POST"])
def create_post_view(request):

    if request.user.is_authenticated:
        if request.method == "POST":
            post = Post(title=request.POST.get("title"), text=request.POST.get("text"), author=request.user)
            post.save()
            return redirect('/')
        else:
            context = {}
            return render(request, "create_post.html", context)
    else:
        return redirect('/')


@require_http_methods(["GET"])
def post_view(request):

    post_id = request.GET.get("id")

    if post_id is not None:
        try:
            post_id = int(post_id)
            post = Post.objects.get(id=post_id)
            post.username = post.author.get_username()
            context = {"post": post}

            return render(request, "post.html", context)
        except ValueError:
            return redirect("/")
        except Post.DoesNotExist:
            return redirect("/")
    else:
        return redirect("/")

