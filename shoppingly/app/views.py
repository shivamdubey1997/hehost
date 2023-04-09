from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views import View
from .models import Customer,Product,Cart,OrderPlaced
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages

from django.contrib.auth.models import User
#def home(request):

 #return render(request, 'app/home.html')
class ProductView(View):

 def get(self,request):
  topwears = Product.objects.filter(category='TW')
  bottomwears = Product.objects.filter(category='BW')
  mobiles = Product.objects.filter(category='M')
  return render(request,'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles})

#def product_detail(request):
 #return render(request, 'app/productdetail.html')
class ProductDetail(View):
 def get(self,request,pk):
  product = Product.objects.get(pk=pk)
  return render(request,'app/productdetail.html',{'product':product})


def add_to_cart(request):
 user=request.user
 product_id=request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user, product=product).save()
 print(product_id)




 return redirect('/cart')

def show_cart(request):
 if request.user.is_authenticated:

  user = request.user
  cart =Cart.objects.filter(user=user)
  print(cart)
  amount = 0.0
  shipping_amount = 70.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user==user]
  #print(cart_product)
  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity* p.product.discount_price)
    amount += tempamount
    totalamount = amount+shipping_amount
   return render(request, 'app/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount})
  else:
   return render(request,'app/emptycart.html')

def plus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']

  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity+=1
  c.save()
  amount = 0.0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
   tempamount = (p.quantity * p.product.discount_price)
   amount += tempamount
   totalamount = amount + shipping_amount
  data = {
   'quantity':c.quantity,
   'amount':amount,
   'totalamount':totalamount
   }
  return JsonResponse(data)


def minus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  print(prod_id)
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity-=1
  c.save()
  amount = 0.0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
   tempamount = (p.quantity * p.product.discount_price)
   amount += tempamount
   totalamount = amount + shipping_amount
  data = {
   'quantity':c.quantity,
   'amount':amount,
   'totalamount':totalamount
   }
  return JsonResponse(data)


def remove_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  print(prod_id)
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))

  c.delete()
  amount = 0.0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
   tempamount = (p.quantity * p.product.discount_price)
   amount += tempamount

  data = {

   'amount':amount,
   'totalamount':amount + shipping_amount
   }
  return JsonResponse(data)








def buy_now(request):
 return render(request, 'app/buynow.html')



def address(request):
 add =Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

def orders(request):
 op = OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html',{'order_placed':op})



def mobile(request,data=None):
 if data == None:

  mobiles = Product.objects.filter(category='M')
 elif data == 'Redmi' or data == 'Samsung':
  mobiles =  Product.objects.filter(category='M').filter(brand=data)
 elif data == 'below':
  mobiles = Product.objects.filter(category='M').filter(discount_price__lt = 10000)
 elif data == 'above':
  mobiles = Product.objects.filter(category='M').filter(discount_price__gt = 10000)

 return render(request, 'app/mobile.html',{'mobiles':mobiles})

def topwear(request,data=None):
 if data == None:

  topwear = Product.objects.filter(category='TW')
 elif data == 'Polo' or data == 'Park':
  topwear =  Product.objects.filter(category='TW').filter(brand=data)
 elif data == 'below':
  topwear = Product.objects.filter(category='TW').filter(discount_price__lt = 1000)
 elif data == 'above':
  topwear = Product.objects.filter(category='TW').filter(discount_price__gt = 1000)

 return render(request, 'app/topwear.html',{'topwear':topwear})


def bottomwear(request,data=None):
 if data == None:
  bottomwear = Product.objects.filter(category='BW')
 elif data== 'Spykar' or data=='Lee':
  bottomwear = Product.objects.filter(category='BW').filter(brand=data)
 elif data == 'below':
  bottomwear = Product.objects.filter(category='BW').filter(discount_price__lt = 1000)
 elif data == 'above':
  bottomwear = Product.objects.filter(category='BW').filter(discount_price__gt = 1000)

 return render(request, 'app/bottomwear.html',{'bottomwear':bottomwear})







class CustomerRegistrationView(View):
 def get(self,request):
  form = CustomerRegistrationForm()
  return render(request,'app/customerregistration.html',{'form':form})
 def post(self,request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request,'Congratulations!! Registered Successfully')
   form.save()
  return render(request, 'app/customerregistration.html', {'form': form})



def checkout(request):
 user = request.user
 add = Customer.objects.filter(user=user)
 cart_items = Cart.objects.filter(user=user)
 amount = 0.0
 shipping_amount = 70.0
 totalamount = 0.0
 cart_product = [p for p in Cart.objects.all() if p.user == request.user]
 if cart_product:
  for p in cart_product:
   tempamount = (p.quantity * p.product.discount_price)
   amount += tempamount
   totalamount = amount + shipping_amount
 return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_item':cart_items})

def payment_done(request):
 user = request.user
 custid = request.GET.get('custid')
 customer = Customer.objects.get(id=custid)
 cart = Cart.objects.filter(user=user)
 for c in cart:
  OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
  c.delete()
 return redirect('orders')

class ProfileView(View):
 def get(self,request):
  form = CustomerProfileForm()
  return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

 def post(self,request):
  form = CustomerProfileForm(request.POST)
  if form.is_valid():
   usr = request.user
   name = form.cleaned_data['name']
   locality = form.cleaned_data['locality']
   city = form.cleaned_data['city']
   state = form.cleaned_data['state']
   zipcode = form.cleaned_data['zipcode']
   reg = Customer(user=usr,name=name,locality=locality,city=city,zipcode=zipcode,state=state)
   reg.save()
   messages.success(request,'Congratulations profile Updated')
  return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})


def article_search_view(request):
 query_dict = request.GET
 # query = query_dict.get("q")
 try:
  query = int(query_dict.get("q"))
 except:
  query = None
 article_obj = None
 if query is not None:
  article_obj = Product.objects.get(id=query)
 context = {
  "product": article_obj,
 }
 return render(request, "app/search.html", context=context)



def services(request):
 services = Product.objects.all()
 if request.method == "GET":
  st = request.GET.get('servicename')
  if st != None:
   services = Product.objects.filter(title__icontains=st)
 return render(request,'app/services.html',{'services': services})
