from django.shortcuts import HttpResponse


def index(req):
    print("Welcome to Django project")
    next = f"<hr><a href='/'>Home</a>\t<a href='/signup'>SignUP</a>\t<a href='#'>SignIN</a> </hr>"
    return HttpResponse(f"<center><h1>My First Django Page</h1>{next}</center>")


def signup(req):
    next = f"<hr><a href='/'>Home</a>\t<a href='/signup'>SignUP</a>\t<a href='#'>SignIN</a> </hr>"
    return HttpResponse(f"<center><h1>SignUP</h1>{next}</center>")
