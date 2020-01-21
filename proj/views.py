from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


# Create your views here.

def index_view(request):
    context = {}
    return render(request, "index.html", context)

