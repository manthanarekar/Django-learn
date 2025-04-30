from django.contrib import admin
from .models import Books

# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display=[
        "userid","bookid","title","author","category","price","qty","dop",
    ]

admin.site.register(Books,BookAdmin)