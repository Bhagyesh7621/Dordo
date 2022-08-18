from asyncio.windows_events import NULL
from distutils.command.upload import upload
from email.mime import image
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MainCategories(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class SubCategories(models.Model):
    mcate = models.ForeignKey(MainCategories,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Product(models.Model):
    pcate = models.ForeignKey(SubCategories,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="image\Product")
    price = models.IntegerField(default=0)
    detail = models.CharField(max_length=600)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product= models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.name

    def prod_total(self):
        return (self.product.price * self.quantity)

class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product= models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.name

    def prod_total(self):
        return (self.product.price * self.quantity)



#Cust Address Model Start

    
class CustomeraddressModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)
    email = models.EmailField()
    mobile = models.IntegerField()
    counrty = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    pincode = models.IntegerField()
    add1 = models.CharField(max_length=200)
    add2 = models.CharField(max_length=200)


    def __str__(self):
        return self.fname


#Cust Address Model end

step = (('Pending','Pending'),('Accepted','Accepted'),('Packing','Packing'),('Shipping','Shipping'),('Deliverd','Deliverd'))

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomeraddressModel,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=step,max_length=200,default='Pending')