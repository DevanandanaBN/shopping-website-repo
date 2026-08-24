from django.shortcuts import render
from shopsphere.form import CustomUserForm
from . models import *
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
import json
def home(request):
    products = Products.objects.filter(trending=1)
    return render(request,"ecom/index.html",{"products":products})
def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,"ecom/cart.html",{"cart":cart})
    else:
         return redirect('/')
def delete_cart(request,cid):
        cartitem=Cart.objects.get(id=cid)
        cartitem.delete()
        return redirect('/cart')
def favviewpage(request):
    if request.user.is_authenticated:
        favourite=Favourite.objects.filter(user=request.user)
        return render(request,"ecom/fav.html",{"favourite":favourite})
    else:
         return redirect('/')

def favourite_page(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            try:
                data = json.loads(request.body)
                product_id = data.get('pid')

                if not product_id:
                    return JsonResponse({'status': 'Product ID is missing'}, status=400)

                try:
                    product = Products.objects.get(id=product_id)
                except Products.DoesNotExist:
                    return JsonResponse({'status': 'Product not found'}, status=404)

                if Favourite.objects.filter(user=request.user, product_id=product_id).exists():
                    return JsonResponse({'status': 'Product is already in favourite'}, status=200)
                else:
                    Favourite.objects.create(user=request.user, product_id=product_id)
                    return JsonResponse({'status': 'Product added to favourite'}, status=201)

            except json.JSONDecodeError:
                return JsonResponse({'status': 'Invalid JSON'}, status=400)

        else:
            return JsonResponse({'status': 'Login required to add favourite'}, status=401)

    return JsonResponse({'status': 'Invalid request method'}, status=405)

def delete_fav(request,fid):
        item=Favourite.objects.get(id=fid)
        item.delete()
        return redirect('/favviewpage')

def add_to_cart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=(data['product_qty'])
            product_id=(data['pid'])
            #print(request.user.id)
            product_status=Products.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'product is already in cart'},status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'product is added to cart'},status=200)
                    else:
                        return JsonResponse({'status':'product is out of stock cart'},status=200)
        else:
            return JsonResponse({'status': 'Login required to add to cart'}, status=401)
    else:
        return JsonResponse({'status':'invalid access'},status=200)


           
def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out Successfully")
        return redirect('/')
def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method=='POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Logged Successfully")
                return redirect('/')
            else:
                messages.error(request,"Invalid username or Password")
                return redirect("/login") 
        return render(request,"ecom/login.html")
def register(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration is successful. You can login now.")
            return redirect('/login')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
            print("Form errors:", form.errors)  
    else:
        form = CustomUserForm()
    
    return render(request, "ecom/register.html", {'form': form})

def collection(request):
    category=Category.objects.filter(status=0)
    return render(request,"ecom/collection.html",{"category":category})
def collectionview(request, name):
    if(Category.objects.filter(name=name, status=0)):
        products = Products.objects.filter(category__name=name)
        return render(request, "ecom/products/index.html", {"products":products,"category_name":name})
    else:
        messages.warning(request, "No Such Category Found")
        return redirect('collection') 
    
def product_details(request, cname, pname):
    if (Category.objects.filter(name=cname, status=0)):
        if (Products.objects.filter(name=pname,status=0)):
            products = Products.objects.filter(name=pname,status=0).first()
            return render(request, 'ecom/products/product_details.html', {"products": products})
        else:
            messages.warning(request, "No Such Product Found")
            return redirect('collection')
    else:
        messages.warning(request, "No Such Category Found")
        return redirect('collection')
