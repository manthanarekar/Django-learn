from django.shortcuts import render,redirect
from .models import Products , ProductImage , Category , Wishlist , Carts , UserProfile, Address
def index(req):
    allproducts = Products.objects.all()
    category = Category.objects.all()
    context = {"allproducts" : allproducts , 'allcategory' : category}
    return render(req,'index.html',context)

from django.contrib import messages
from django.contrib.auth.models import User
from .models import CustomUser

def signup(req):
    print(req.method)
    if req.method == "POST":
        print(req.method)
        uname = req.POST.get("uname")
        uemail = req.POST.get("uemail")
        upass = req.POST.get("upass")
        ucpass = req.POST.get("ucpass")
        print(uname, uemail, upass, ucpass)
        user = CustomUser.objects.values_list("username", flat=True)
        print(user)
        chkemail = CustomUser.objects.values_list("email", flat=True)
        print(chkemail)

        if upass != ucpass:
            # errmsg="Password and Confirm Password doesn't match. Try again"
            # context={'errmsg':errmsg}
            # return render(req,'signup.html',context)

            messages.error(
                req, "Password and Confirm Password doesn't match.TRY again "
            )
            return render(req, "signup.html")
        elif uname == upass:
            messages.error(req, " Username and Password be different")
            return render(req, "signup.html")
        elif uname in user:
            messages.error(req, " Username already exists. Try again")
            return render(req, "signup.html")
        elif uemail in chkemail:
            messages.error(req, " Email already exists")
            return render(req, "signup.html")

        newuser = CustomUser.objects.create(username=uname, email=uemail, password=upass, is_customer=True )
        newuser.set_password(upass)
        newuser.save()
        print(CustomUser.objects.all())

        messages.success(req, "Registration done Successfully!! ")
        return redirect("signin")

    else:
        print(req.method)
        return render(req, "signup.html")


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password

def signin(req):
    if req.method == 'POST':
        user_type = req.POST.get('user_type')
        uemail = req.POST.get('uemail')
        upass = req.POST.get('upass')
        print(user_type,uemail,upass)
        try:
            chkemail = CustomUser.objects.get(email=uemail)
            print(chkemail)
            if chkemail.check_password(upass):
                login(req, chkemail)
                if user_type == "admin":
                    if chkemail.is_staff:
                        return redirect('/admin')
                    else:
                        messages.error(req,"Invalid email or password")
                        return render(req,'signin.html')
                    
                if user_type == 'customer':
                    return redirect('/')
            else:
                messages.error(req, "Invalid email or password")
                return render(req, "signin.html")
        except User.DoesNotExist:
            messages.error(req, "User Not exists")
            return render(req, "signin.html")
        
    return render(req,'signin.html')


def userlogout(req):
    logout(req)
    return redirect("/")

def seller(req):
    user = req.user
    chkuser = CustomUser.objects.get(username = user)
    if chkuser.is_seller:
        return render(req,"seller.html")
    else:
        return render(req,'seller_payment.html')
    
def seller_payment(req):
    if req.method == 'POST':
        chkuser = CustomUser.objects.get(username = req.user)
        chkuser.is_seller = True
        chkuser.save()
        return redirect('seller')
    else:
        return render(req,'seller_payment.html')
    
from django.db.models import Q

def searchproduct(req):
    query = req.GET["q"]
    if query:
        allproducts = Products.objects.filter(
            Q(productname__icontains = query ) | Q(description__icontains = query)
        )
        allcategory = Category.objects.all()

        if len(allproducts) == 0:
            messages.error(req,'No result found!')
            context = {'allcategory' : allcategory }
            return render(req,'index.html',context )
    
    else:
        allproducts = Products.objects.all()
        allcategory = Category.objects.all()
    context = {"allproducts" : allproducts , 'allcategory' : allcategory}
    return render(req,'index.html',context)

def electronic_search(req):
    ele_category = Category.objects.filter(name='Electronics').first()
    allproducts = Products.objects.filter(category = ele_category)
    allcategory = Category.objects.all()
    if len(allproducts) == 0:
        messages.error(req,'No result found!')
    context = {"allproducts" : allproducts , 'allcategory' : allcategory}
    return render(req,'index.html',context)


def cloth_list(req):
    allproducts = Products.productmanager.cloths_search()
    allcategory = Category.objects.all()

    if len(allproducts) == 0:
        messages.error(req,'No result found!')
        
    context = {"allproducts" : allproducts , 'allcategory' : allcategory}
    return render(req,'index.html',context)


def shoes_list(req):
    allproducts = Products.productmanager.shoes_filter()
    allcategory = Category.objects.all()

    if len(allproducts) == 0:
        messages.error(req,'No result found!')
        
    context = {"allproducts" : allproducts , 'allcategory' : allcategory}
    return render(req,'index.html',context)

def searchby_price_range(req):
    min = req.GET['min']
    max = req.GET['max']
    allcategory = Category.objects.all()
    if max is not None and min is not None :
        allproducts = Products.productmanager.price_range(min,max)
        
        if len(allproducts) == 0:
            messages.error(req,'No result found!')
        
    context = {"allproducts" : allproducts , 'allcategory' : allcategory}
    return render(req,'index.html',context)


def sortbyprice(req):
    sortoption = req.GET['sort']
    if sortoption == 'low_to_high':
        allproducts = Products.objects.order_by("price")
    elif sortoption == 'high_to_low':
        allproducts = Products.objects.order_by("-price")
    else:
        allproducts = Products.objects.all()
        
    allcategory = Category.objects.all()
    context = {"allproducts" : allproducts , 'allcategory' : allcategory}
    return render(req,'index.html',context)

def productdetails(req,productid):
    product = Products.objects.get(productid = productid)
    productimg = ProductImage.objects.filter(productid = productid)
    context = {'product':product , 'productimg' : productimg}
    return render(req, 'product_details.html',context)

def show_wishlist(req):
    if req.user.is_authenticated:
        user = req.user
        wishlist_item = Wishlist.objects.filter(user = user)
        context = {'wishlist_item' : wishlist_item}
        if len(wishlist_item) == 0:
            messages.error(req,'No items select yet!')
            
        return render(req, "wishlist_item.html" , context)
    else:
        return redirect('signin')
    
from django.shortcuts import get_object_or_404
def addtowishlist(req, productid):
    if req.user.is_authenticated:
        user = req.user
        product = get_object_or_404(Products, productid = productid)
        if not Wishlist.objects.filter(user = req.user , productid = productid).exists():
            Wishlist.objects.create(user= user, productid = product)
            messages.success(req,'Product added to Wishlist')
        else:
            messages.info(req,'Product is alredy in wishlist')
        
        return redirect('show_wishlist')
    else:
        return redirect('signin')
    
def removefromwishlist(req, productid):
    if req.user.is_authenticated:
        user = req.user
        product = get_object_or_404(Products, productid = productid)
        wishlist_item = Wishlist.objects.filter(user = user , productid = product )
        wishlist_item.delete()
        messages.success(req,"Product removed from wishlist")
        return redirect('show_wishlist')
    else:
        return redirect('signin')
    
from datetime import datetime , timedelta
    
def showcart(req):
    if req.user.is_authenticated:
        user = req.user
        cart_list =Carts.objects.filter(user = user)
        today_date = datetime.today()
        future_date = today_date + timedelta(days = 4)
        
        totalitems = cart_list.count()
        totalamount = sum(x.productid.price*x.qty for x in cart_list)
        has_profile = UserProfile.objects.filter(user = user).exists()
        has_address = Address.objects.filter(user = user).exists()
        
        context = {'cart_list' : cart_list ,
                   'future_date' : future_date , 
                   "totalitems" : totalitems , 
                   'totalamount' : totalamount , 
                   'has_profile' : has_profile , 
                   'has_address' : has_address ,
                   }     
        
        return render(req,'showcarts.html', context)
    else:
        redirect('signin')
        
def updateqty(req,qv,productid):
    product = get_object_or_404(Products , productid = productid)
    allcarts = Carts.objects.filter(productid = productid , user = req.user)
    cart_item = allcarts.first()
    if qv == 1:
        if cart_item.qty < product.qty_available:
            cart_item.qty += 1
            cart_item.save()
            
        else:
            messages.error(req, 'Only limied stock available')
    else:
        if cart_item.qty > 1:
            cart_item.qty -= 1
            cart_item.save()
        else:
            cart_item.delete()
    
    return redirect("showcart")        
    
def addtocart(req,productid):
    if req.user.is_authenticated:
        user = req.user
        product = get_object_or_404(Products, productid=productid)
        cartitem, created = Carts.objects.get_or_create(user = user , productid = product )
        new_qty = cartitem.qty + 1 if not created else 1
        if new_qty > product.qty_available:
            messages.error(req,'Cannot add more item-only limited stock available')
            return redirect('showcart')

        cartitem.qty = new_qty
        cartitem.save()
        return redirect('showcart')
    else:
        return redirect('signin')
        
def removeproductcart(req,productid):
    if req.user.is_authenticated:
        user = req.user
        product = get_object_or_404(Products, productid=productid)
        cartitem= Carts.objects.filter(user = user , productid = product )
        cartitem.delete()
        messages.success(req, "Prodcut removed from cart.")
        return redirect('showcart')

    else:
        return redirect('signin')
    
def myprofile(req):
    user = req.user
    userprofile = UserProfile.objects.filter(user = user).first()
    address = Address.objects.filter(user= user)
    context = {'user':user,'userprofile':userprofile, 'address':address}
    return render(req,'myprofile.html',context)


def addprofiile(req):
    user = req.user
    if req.method == 'POST':
        mobile = req.POST.get("Mobile")
        gender = req.POST.get("gender")
        dob = req.POST.get("dob")
        photo = req.FILES["photo"]
        UserProfile.objects.create(user=user,mobile = mobile , gender= gender , dob = dob , photo = photo)
        return redirect('myprofile')
    else:
        return render(req,"addprofile.html")