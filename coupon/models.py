
from django.db import models
from django.utils import timezone
from adminapp.models import Category
from accounts.models import CustomUser 
# Import your Category model


# Create your models here.


class Coupon(models.Model):

    DISCOUNT_TYPES = (
        ('percentage', 'Percentage'),
        ('amount', 'Amount'),
    )

    APPLICABLE_TYPES = (
        ('all', 'Category All'),
        ('category', 'Category'), 
    )

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPES)
    discount = models.DecimalField(max_digits=10, decimal_places=0)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    applicable_type = models.CharField(max_length=10, choices=APPLICABLE_TYPES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, default=None, null=True, blank=True)
    min_purchase = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, default=0)
    max_amount = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, default=0)

    # New fields
    usage_limit = models.PositiveIntegerField(default=0)
    times_used = models.PositiveIntegerField(default=0)

    def is_valid(self):
        current_time = timezone.now()
        return self.is_active and self.start_date <= current_time and self.end_date >= current_time

    def is_applicable_to_order(self, order_amount, order_category):
        if not self.is_valid():
            return False

        if self.applicable_type == 'all':
            return True
        elif self.applicable_type == 'category' and self.category == order_category:
            return True
        
        return False
    
    def can_be_applied(self):
        return self.times_used < self.usage_limit or self.usage_limit == 0

    def __str__(self):
        return self.name
    

class UserCoupon(models.Model):
    user= models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    coupon_applied = models.ForeignKey(Coupon,on_delete=models.CASCADE)
    is_applied = models.BooleanField(default=True)
    
    # models.py

from django.db import models

class Discount(models.Model):
    total_discount = models.DecimalField(max_digits=10, decimal_places=2)
    # Add any additional fields you need, such as a reference to the order or user.

    def __str__(self):
        return f"Total Discount: ₹{self.total_discount}"


    
    

