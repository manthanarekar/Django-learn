from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('signup/',views.signup,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    # path("",views.DTldemo)
]
