from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import messages

class Register(AbstractUser):
    FirstName=models.CharField(max_length=20,null=True)
    LastName=models.CharField(max_length=20,null=True)
    phone=models.IntegerField(null=True)
    usertype=models.CharField(default="admin",max_length=10)
        

class Product(models.Model):
    seller = models.ForeignKey(Register, on_delete=models.CASCADE, null=True, blank=True)
    name=models.CharField(max_length=20,null=True)
    price=models.IntegerField(null=True)
    description=models.CharField(max_length=100,null=True)
    warranty=models.IntegerField(null=True)
    image = models.ImageField(upload_to="uploads/",null=True)

    
class Cart(models.Model):
    user = models.ForeignKey(Register,on_delete=models.CASCADE,related_name="user_cart")
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="cart_products")
    added_at = models.DateTimeField(auto_now_add=True)
    quantity=models.IntegerField(default=1)
  

class Order(models.Model):
    userid = models.ForeignKey(Register, on_delete=models.CASCADE, null=True, blank=True)    
    date = models.DateTimeField(auto_now_add=True)
    totalamount=models.IntegerField(default=0)

class OrderItem(models.Model):
    orderid = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)    
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="order_product")
    quantity = models.IntegerField(default=1)
    returned = models.BooleanField(default=False)
    return_date = models.DateTimeField(null=True, blank=True)

class Feedback(models.Model):
    userid =models.ForeignKey(Register,on_delete=models.CASCADE,related_name="user_item")
    orderid =models.ForeignKey(Order,on_delete=models.CASCADE,related_name="order_item")
    seller = models.ForeignKey(Register, on_delete=models.CASCADE, null=True, blank=True)    
    rating=models.IntegerField(default=1)
    date=models.DateTimeField(auto_now_add=True)
    message=models.TextField(default="")