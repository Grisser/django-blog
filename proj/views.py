from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from proj.models import Post


# Create your views here.

def index_view(request):
    context = {}
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
