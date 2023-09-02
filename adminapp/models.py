from django.db import models




# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)

class Brands(models.Model):
    brand_name = models.CharField(max_length=50)
    from django.db import models


    
    


class Products(models.Model):
    product_name = models.CharField(max_length=50)
    product_brand = models.ForeignKey(Brands,on_delete=models.CASCADE)
    product_category = models.ForeignKey(Category,on_delete=models.CASCADE)
    
    product_price = models.IntegerField(default=0)
    quantity = models.IntegerField()
    product_details = models.TextField(max_length=2000,blank=True)
    product_image = models.ImageField(upload_to = 'product_image/',default = None,blank = True,null = True)
    offer_price = models.IntegerField(blank=True,null=True)
    product_status = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0) 
    is_available = models.BooleanField(default=True)
    offer_start_date = models.DateField(blank=True, null=True)
    offer_end_date = models.DateField(blank=True, null=True)
    
    


class ProductImage(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    
    def __str__(self):
        return self.product.product_name

 
