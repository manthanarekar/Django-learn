from django.shortcuts import render, HttpResponse


# Create your views here.
def index(request):
    next = f'<a href="/">Home<a>\t<a href="/events">Event<a>'
    return HttpResponse(
        f"<center><h1>Welcome to books app.</h1><hr>{next}</hr></center>"
    )
