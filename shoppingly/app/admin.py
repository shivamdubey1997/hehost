from django.contrib import admin
from .models import (Customer,Product,Cart,OrderPlaced)
# Register your models here.
@admin.register(Customer)
class CustomerModelAmin(admin.ModelAdmin):
    list_display = ['id','user','name','locality','city','zipcode','state']

@admin.register(Product)
class CustomerModelAmin(admin.ModelAdmin):
    list_display = ['id','title','selling_price','discount_price','description','brand','category','product_image']

@admin.register(Cart)
class CustomerModelAmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']

@admin.register(OrderPlaced)
class CustomerModelAmin(admin.ModelAdmin):
    list_display = ['id','user','customer','product','quantity','order_date','status']