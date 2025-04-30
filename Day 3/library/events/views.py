from django.shortcuts import render, HttpResponse

# Create your views here.


def index(request):
    next = f'<a href="/events">Home<a>\t<a href="/">Books<a>'
    return HttpResponse(
        f"<center><h1>Welcome to Events app.</h1><hr>{next}</hr></center>"
    )
