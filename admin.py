from django.contrib import admin
from .models import MainCategories, Order, Product,SubCategories, Cart, Wishlist, CustomeraddressModel
# Register your models here.


@admin.register(MainCategories)
class MainCategoriesAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(SubCategories)
class SubCategoriesAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name","image","price","detail", "pcate"]



@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["quantity", "product", "user"][::-1]


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ["prod_total","quantity", "product", "user"][::-1]




@admin.register(CustomeraddressModel)
class CustomeraddressModelAdmin(admin.ModelAdmin):
    list_display = ("add2", "add1", "pincode", "city", "state", "counrty", "mobile", "email", "lname", "fname", "user")[::-1]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["status", "order_date", "quantity", "product", "customer", "user"][::-1]



