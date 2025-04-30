from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "index.html")


def signup(request):
    return render(request, "signup.html")


def signin(req):
    return render(req, "signin.html")


def about(req):
    return render(req, "about.html")


def contact(req):
    return render(req, "contact.html")
