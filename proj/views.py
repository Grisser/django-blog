from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from proj.models import *


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
            title = request.POST.get("title")
            text = request.POST.get("text")

            if (title is not None) and (text is not None):
                post = Post(title=request.POST.get("title"), text=request.POST.get("text"), author=request.user)
                post.save()

            return redirect('/')
        else:
            context = {}
            return render(request, "create_post.html", context)
    else:
        return redirect('/')


@require_http_methods(["GET", "POST"])
def post_view(request):

    if request.method == "GET":

        post_id = request.GET.get("id")

        if post_id is not None:
            try:
                post_id = int(post_id)
                post = Post.objects.get(id=post_id)
                post.username = post.author.get_username()

                likes = Like.objects.all().filter(post_id=post_id)
                likes_count = len(likes)

                liked = False
                likes_text = ""

                if request.user.is_authenticated:
                    for like in likes:
                        if like.author_id == request.user.id:
                            liked = True

                if (likes_count == 1 or (likes_count > 20 and (likes_count % 10) == 1) or (likes_count % 100) != 11) and \
                        (likes_count != 0):
                    likes_text = "пользователю"
                else:
                    likes_text = "пользователям"

                comments = Comment.objects.all().filter(post_id=post_id)
                context = {"post": post, "comments": comments, "likes": likes_count, "likes_text": likes_text, "liked": liked}

                return render(request, "post.html", context)
            except ValueError:
                return redirect("/")
            except Post.DoesNotExist:
                return redirect("/")
        else:
            return redirect("/")
    else:
        post_id = request.POST.get("post_id")
        text = request.POST.get("text")

        if post_id is not None and request.user.is_authenticated:
            try:
                post_id = int(post_id)
                post = Post.objects.get(id=post_id)
                comment = Comment(text=text, post=post, author=request.user)

                comment.save()
            except ValueError:
                pass
            except Post.DoesNotExist:
                pass

        return redirect("/post?id=" + str(post_id) + "#commentaries")

@require_http_methods(["GET"])
def like_view(request):

    if request.user.is_authenticated:

        try:
            post_id = int(request.GET.get("post"))
            post = Post.objects.get(id=post_id)
            like = Like.objects.get(post=post, author=request.user)
            like.delete()

            return redirect("/post?id=" + str(post_id) + "#like")
        except Like.DoesNotExist:
            like = Like(post=post, author=request.user)
            like.save()

            return redirect("/post?id=" + str(post_id) + "#like")
        except Post.DoesNotExist:
            return redirect("/")
        except ValueError:
            return redirect("/")

    else:
        return redirect("/accounts/login")
