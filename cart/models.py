from django.db import models
from adminapp.models import Products
from accounts.models import CustomUser
from coupon.models import Coupon


# Create your models here.
# models.py

class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateField(auto_now_add=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return self.cart_id  
    
    def total(self):
        cart_items = self.cartitem_set.all()
        total = sum(cart_item.product.product_price * cart_item.quantity for cart_item in cart_items)
        return total

class CartItem(models.Model): 
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    
    
    def sub_total(self):
        return self.product.product_price * self.quantity

    def __str__(self):
        return str(self.product)


class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    address_line_1 = models.CharField(max_length=100, null=True, blank=True)
    address_line_2 = models.CharField(max_length=100, null=True, blank=True)
    postcode = models.CharField(max_length=10, null=True, blank=True)
    area = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name

class whishlist(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  
        
    
        
    