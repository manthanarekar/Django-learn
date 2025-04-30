from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Books(models.Model):
    userid = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,default=None)
    bookid = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    type = (('Progamming','Programming'),('Database','Database'),('Networking','Networking'))
    category = models.CharField(max_length=50,choices=type)
    price = models.FloatField() 
    qty = models.PositiveIntegerField(default=0)
    dop = models.DateField()   