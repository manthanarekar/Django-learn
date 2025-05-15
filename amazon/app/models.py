from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.
from django.contrib.auth.models import User, AbstractUser

class CustomUser(AbstractUser):
    is_customer=models.BooleanField(default=False)
    is_seller=models.BooleanField(default=False)
    class Meta:
        verbose_name='CustomUser'

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    mobile = models.PositiveIntegerField(validators=[MinValueValidator(6000000000),MaxValueValidator(9999999999)])
    type = (('Male','Male'),('Female','Female'),('Other','Other'))
    gender = models.CharField(max_length=50,choices=type)
    dob = models.DateField(null=True,default=None)
    photo = models.ImageField(upload_to='images',null=True,default=None)

class Country(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country,on_delete=models.SET_NULL,null=True,default=None)
    def __str__(self):
        return self.name
    
from django.conf import settings
class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.TextField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    pincode = models.PositiveIntegerField(
        validators=[MinValueValidator(100000),MaxValueValidator(999999)]
        )
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    type = (('Male','Male'),('Female','Female'),('None','None'))
    gender = models.CharField(max_length=30,choices=type)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, default=None
    )
    def __str__(self):
        return self.name
    
class Products(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,default=None)
    productid = models.PositiveIntegerField(primary_key=True)
    productname = models.CharField(max_length=50)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, default=None
    )
    subcategory=models.ForeignKey(
        SubCategory, on_delete=models.SET_NULL, null=True, default=None
    )
    description = models.TextField()
    price = models.FloatField()
    qty_available = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.productname

class ProductImage(models.Model):
    productid = models.ForeignKey(Products, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.productid.productname
    
class Carts(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,default=None)
    productid =  models.ForeignKey(Products, on_delete=models.CASCADE)

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,default=None)
    productid = models.ForeignKey(Products, on_delete=models.CASCADE)
