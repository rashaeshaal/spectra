from django.db import models
from adminapp.models import Products
from accounts.models import CustomUser
from cart.models import Address
from django.db import models
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _
from .constants import PaymentStatus




# Create your models here.

class Order(models.Model):   
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELED', 'Canceled'),
    )
    
    PAYMENT_METHOD_CHOICES = (
        ('cod', 'Cash on Delivery'),
        ('razorpay', 'Razorpay'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    payment_mode = models.BooleanField(default=True)
    is_canceled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Processing')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    
      
      
      
    def cancel_order(self):
            # Update order status to 'CANCELLED'
        self.status = 'CANCELLED'
        self.save()
    
   

    def __str__(self):
        return f"Order {self.id} - {self.user.first_name} "

    
class OrderItem(models.Model):
    order_no = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    product_price = models.IntegerField(null=True)



    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order: {self.order_no.id})"

    def total_price(self):
        return self.product.price * self.quantity
    
    
class Orders(models.Model):
    name = CharField(_("Customer Name"), max_length=254, blank=False, null=False)
    amount = models.FloatField(_("Amount"), null=False, blank=False)
    status = CharField(
        _("Payment Status"),
        default=PaymentStatus.PENDING,
        max_length=254,
        blank=False,
        null=False,
    )
    provider_order_id = models.CharField(
        _("Order ID"), max_length=40, null=False, blank=False
    )
    payment_id = models.CharField(
        _("Payment ID"), max_length=36, null=False, blank=False
    )
    signature_id = models.CharField(
        _("Signature ID"), max_length=128, null=False, blank=False
    )

    def __str__(self):
        return f"{self.id}-{self.name}-{self.status}"

    
   