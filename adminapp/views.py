from django.shortcuts import render,redirect
from .forms import CategoryForm
from .models import Category,Brands,ProductImage
from django.shortcuts import render, get_object_or_404, redirect
from .models import Products,ProductImage
from .forms import ProductGalleryForm
from django.views.decorators.cache import never_cache
from accounts.models import CustomUser
from django.contrib.auth.models import User
from django.http import JsonResponse
from orders.models import Order,OrderItem
from cart.models import Address
from django.contrib import messages
from coupon.models import Coupon
import json
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Count, F
from orders.models import OrderItem 
from django.db import models
from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render
from datetime import datetime
from django.contrib.auth.decorators import login_required





@login_required(login_url='admin_signin')
def admin_dashboard(request):
    status_order_totals = Order.objects.values('status').annotate(total_amount=Sum('total_amount'))

    context = {
        'status_order_totals': status_order_totals,
    }
   
    return render(request, 'admintemp/admin_dashboard.html', context)



def sales_report(request):
    sales_report_data = Order.objects.all().order_by('-order_date')
    
    return render(request, 'admintemp/salesreport.html',{'sales_report': sales_report_data})



def product_gallery_list(request):
    # Retrieve all products
    products = Products.objects.all()

    # Create a dictionary to store product images for each product
    product_images = {}

    # Loop through products and fetch their associated images
    for product in products:
        images = ProductImage.objects.filter(product=product)
        product_images[product] = images

    context = {
        'products': products,
        'product_images': product_images,
    }

    return render(request, 'admintemp/image_gallery.html', context)

def edit_gallery(request, product_id):
    product = get_object_or_404(Products, pk=product_id)
    product_images = ProductImage.objects.filter(product=product)

    if request.method == 'POST':
        # Handle form submission
        new_images = request.FILES.getlist('new_images')

        # Update the existing images with the new ones
        for image in new_images:
            # Create a new ProductImage instance or update an existing one
            product_image = ProductImage(product=product, image=image)
            product_image.save()

        return redirect('product_gallery_list')

    context = {
        'product': product,
        'product_images': product_images,
    }

   
    return render(request, 'admintemp/edit_gallery.html', context)

def add_gallery(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        images = request.FILES.getlist('image')

        if product_id and images:
            product = Products.objects.get(id=product_id)

            for image in images:
                gallery_item = ProductImage(product=product, image=image)
                gallery_item.save()

            return redirect('product_gallery_list')  # Redirect to the product gallery list

    # If it's a GET request or if there was an issue with the form submission, display the form
    products = Products.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'admintemp/add_gallery.html', context)



def delete_product(request, product_id):
    # Get the product associated with the given product_id
    product = get_object_or_404(Products, pk=product_id)

    if request.method == 'POST':
        # Handle the POST request to delete the product
        # You can add logic here to delete the product and associated images
        # After deletion, redirect to the product gallery list or any other appropriate page
        product.delete()
        return redirect('product_gallery_list')

    context = {
        'product': product,
    }

    return render(request, 'admintemp/delete_product.html', context)

def delete_image(request, image_id):
    # Get the image associated with the given image_id
    image = get_object_or_404(ProductImage, pk=image_id)

    if request.method == 'POST':
        # Handle the POST request to delete the image
        # You can add logic here to delete the image
        # After deletion, redirect to the product gallery list or any other appropriate page
        image.delete()
        return redirect('product_gallery_list')

    context = {
        'image': image,
    }

    return render(request, 'admintemp/delete_image.html', context)


def edit_brand(request, brand_id):
    brand = get_object_or_404(Brands, id=brand_id)

    if request.method == 'POST':
        brand_name = request.POST.get('brand_name')  # Assuming the input field in the form has name="brand_name"
        brand.brand_name = brand_name
        brand.save()
        return redirect('brand_list')  # Replace 'brand_list' with the URL name of the page showing the list of brands

    context = {
        'brand': brand,
    }

    return render(request, 'admintemp/brands.html', context)

def orderdetails(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        order = get_object_or_404(Order, id=order_id)
        order.status = new_status
        order.save()
        messages.success(request, 'Order status updated successfully.')
        return redirect('order_details')

    statuses = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    orders = Order.objects.all().order_by('-created_at')
    context = {
        'statuses': statuses,
        'orders': orders,
    }
    return render(request, 'admintemp/orderdetails.html', context)

# def orderview(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     order_items = OrderItem.objects.filter(order_no=order)

#     if request.method == 'POST':
#         if 'cancel_order' in request.POST:
#             order.cancel_order()
#             messages.success(request, 'Order has been cancelled successfully.')
#             return redirect('order_detail', order_id=order_id)
#         statuses = [
#         ('pending', 'Pending'),
#         ('processing', 'Processing'),
#         ('shipped', 'Shipped'),
#         ('delivered', 'Delivered'),
#         ('cancelled', 'Cancelled'),
#     ]
#     orders = Order.objects.all().order_by('-created_at')

#     context = {
#         'order': order, 
#         'order_items': order_items,
#         'statuses': statuses,
#         'orders': orders,
#         }
#     return render(request, 'admintemp/orderview.html', context)

def orderview(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order_no=order)

    statuses = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    if request.method == 'POST':
        if 'cancel_order' in request.POST:
            order.cancel_order()
            messages.success(request, 'Order has been cancelled successfully.')
            return redirect('orderview', order_id=order_id)

    context = {'order': order, 'order_items': order_items, 'statuses': statuses}
    return render(request, 'admintemp/orderview.html', context)



def add_brand(request):
    print("add brand")
    if request.method =='POST':
        brand_name = request.POST.get('brand_name')
        brand = Brands(brand_name=brand_name)
        brand.save()
        return redirect('brandslist')
 
 

    
   
def admin_signin(request):
    print('00000000000000000000000000000000000000')
    if request.user.is_authenticated and request.user.is_superuser:
        print('11111111111111111111111111')
        return redirect('admin_dashboard')

    if request.method == 'POST':
        print('2222222222222222')
        username = request.POST.get('Username')
        password = request.POST.get('password')
        user = authenticate(request, email=username, password=password)

        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                return redirect('admin_login')
        else:
            # Handle the case when authentication fails
            return redirect('admin_login')

    return render(request, "admintemp/signin.html")

        
    
    
def admin_logout(request):
    logout(request)
    return redirect('admin_signin')


def user_details(request):
    data = CustomUser.objects.all()
    return render(request,'admintemp/user.html',{'data':data})


def categorylist(request):
    categories=Category.objects.all()
    print("categorylist")
    if request.user.is_superuser:
        categories=Category.objects.all()
    return render(request,'admintemp/category.html',{'categories':categories})


    
def productlist(request):
    product = Products.objects.all()
    brand = Brands.objects.all()
    categories = Category.objects.all()
    for p in product:
        print("Product ID:", p.id)
    if request.user.is_superuser:
        product = Products.objects.all()
        brand = Brands.objects.all()
        categories = Category.objects.all()
        
    
    return render(request, 'admintemp/producttable.html', { 'brand': brand, 'categories': categories,'product':product})







def add_category(request):
    print("add category")
    print(11111111111111111111111111111111)
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        print(category_name,'000000000000000000000000000000000')
        category = Category(name = category_name)
        category.save()
        return redirect(categorylist)
        
    
    
    return render(request, 'admintemp/category.html')

def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('admintemp/category.html')


def edit_category(request, category_id):
    print("edit category")
    if request.method == 'POST':
        edited_category_name = request.POST.get('category_name')
        category = Category.objects.get(id=category_id)
        category.category_name = edited_category_name
        category.save()
        return redirect('categorylist')
    
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'admintemp/category.html', context)

def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_category_id = request.POST.get('product_category')
        product_brand_id = request.POST.get('product_brand')
        product_details = request.POST.get('product_description')
        product_price = request.POST.get('product_mrp')
        quantity = request.POST.get('product_quantity')
        offer_price = request.POST.get('product_offer_price')
        product_brand_name = Brands.objects.get(id=product_brand_id)
        product_category_name = Category.objects.get(id=product_category_id)       
        product_image = request.FILES.get('product_image')
        # print(product_price,quantity,offer_price,product_brand_name,product_category_name,product_details)
        product = Products(
            product_name=product_name,
            product_category=product_category_name,
            product_brand=product_brand_name,
            product_price=product_price,
            quantity=quantity,
            product_details=product_details,
            product_image=product_image,
            offer_price=offer_price
        )
        product.save()
        # for image in product_image:
        #     ProductImage.objects.create(product=product, image=image)

        return redirect('productlist')
    
    return render(request, "admintemp/producttable.html")
@never_cache
def brandslist(request):
    print("brandlist")
    brand = Brands.objects.all()
    if request.user.is_superuser:
        brand = Brands.objects.all()
    return render(request,"admintemp/brands.html",{'brand':brand})


def user_block(request,user_id):
        user = CustomUser.objects.get(id=user_id)
        user.is_active = False
        user.save()
        return redirect(user_details)
    
def user_unblock(request,user_id):
        user= CustomUser.objects.get(id=user_id)
        user.is_active = True
        user.save() 
        return redirect(user_details)
    
    


def edit_product(request,id):
    product = get_object_or_404(Products, id=id)
    print("33333333333333333333333333")

    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        brand_id = request.POST.get('brand')  # Use 'brand' instead of 'product_brand'
        category_id = request.POST.get('category')  # Use 'category' instead of 'product_category'
        product_price = request.POST.get('product_mrp')
        quantity = request.POST.get('product_quantity')
        product_description = request.POST.get('product_description')
        print(brand_id,category_id,product_price,quantity,product_description,"0000000000000000000")

        # Retrieve the updated 'images' field value
        product_thumbnail = request.FILES.get('product_thumbnail')

        # Update other product details
        product.product_name = product_name
        product.product_brand = get_object_or_404(Brands, id=brand_id)
        product.product_category = get_object_or_404(Category, id=category_id)
        product.product_price = product_price
        product.quantity = quantity
        product.product_details = product_description


        # Only update 'images' if a new file was provided
        if product_thumbnail:
            product.images = product_thumbnail

        # Save the updated product
        product.save()

        return redirect('productlist')

    return render(request, 'admintemp/producttable.html', {'product': product})



def delete_product(request, product_id):
    if request.method == 'POST':
        try:
            product = Products.objects.get(pk=product_id)
            product.delete()
            return redirect('productlist')  # Replace 'product_list' with the appropriate URL name
        except Products.DoesNotExist:
            # Handle the case when the product does not exist
            pass

    return redirect('productlist')  # Replace 'product_list' with the appropriate URL name

   
def cancel_order(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
        if order.is_ordered:
            messages.warning(request, 'Order is not yet placed. Cannot be canceled.')
        elif order.is_canceled:
                messages.warning(request, 'Order is already canceled.')
        else:
            # Perform any additional cancellation logic here, if needed.
            # For example, you might want to update the stock quantity of the products associated with the canceled order.

            # Set the order as canceled
            order.is_canceled = True
            order.save()

            # Add a success message to indicate that the order has been canceled.
            messages.success(request, 'Order has been canceled successfully.')
    except Order.DoesNotExist:
        # If the order with the given order_id does not exist, handle the error gracefully.
        messages.error(request, 'Order does not exist.')

            
    return redirect('orderdetails')
def manage_order(request):
    orders = Order.objects.all()
    statuses = Order.STATUS_CHOICES
    
    context = {
        'orders' : orders,
        'statuses' : statuses,
    }
    return render(request, "admintemp/orderdetails.html",context)

def manage_orderstatus(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order_status = request.POST.get('status')
        order.status = order_status
        order.save()
        messages.success(request, 'Order status updated successfully.')
        
        return redirect('manage_order')  # Redirect after successful update

    # Pass the updated context to the template
    orders = Order.objects.all()
    statuses = Order.STATUS_CHOICES
    context = {
        'orders': orders,
        'statuses': statuses,
    }
    return render(request, "admintemp/orderdetails.html", context)





def product_block(request,id):
    block = Products.objects.filter(id=id).update(is_available=False)
    return redirect("productlist")

def product_unblock(request,id):
    un_block = Products.objects.filter(id=id).update(is_available=True)
    return redirect("productlist")



def coupon_list(request):
    coupons = Coupon.objects.all()
    coupon_DISCOUNT_TYPES = Coupon.DISCOUNT_TYPES
    category = Category.objects.all()
    context={
        "coupons": coupons,
        "discount_types": coupon_DISCOUNT_TYPES,
        "category":category,
    }
    return render(request,"admintemp/coupontable.html",context)

def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect('orderdetails') 


def add_coupon(request):
    if request.method == "POST":
        
        coupon_name = request.POST.get('coupon_name')
        coupon_code = request.POST.get('coupon_code')

        coupon_description = request.POST.get('coupon_description')
        coupon_discount_type = request.POST.get('coupon_discount_type')
        coupon_discount = request.POST.get('discount')
        coupon_start_date = request.POST.get('start_date')
        coupon_end_date = request.POST.get('end_date')
        coupon_is_active = request.POST.get('is_active')
        coupon_applicable_type = request.POST.get('applicable_type')
        coupon_category_id = request.POST.get('category')
        coupon_min_amount = request.POST.get('min_amount')
        coupon_max_amount = request.POST.get('max_amount')

        
        coupon = Coupon(
            name=coupon_name,
            code =  coupon_code,
            description=coupon_description,
            discount_type=coupon_discount_type,
            discount=coupon_discount,
            start_date=coupon_start_date,
            end_date=coupon_end_date,
            is_active=bool(coupon_is_active),  # Convert 'true'/'false' to boolean. in  Django's bool() function can be used to convert the string 'true' to the boolean value True and the string 'false' to the boolean value False.
            applicable_type=coupon_applicable_type,
            category_id=coupon_category_id,  # Assign the category ID to the foreign key
            min_purchase=coupon_min_amount,
            max_amount =coupon_max_amount
        )
        coupon.save()
        return redirect('coupon_list')
    return render(request, "admintemp/coupontable.html")


def edit_coupon(request, coupon_id):
    if request.method == "POST":
        edit_coupon_name = request.POST.get('coupon_name')
        edit_coupon_code = request.POST.get('coupon_code')
        edit_coupon_description = request.POST.get('coupon_description')
        edit_coupon_discount_type = request.POST.get('coupon_discount_type')
        edit_coupon_discount = request.POST.get('discount')
        edit_coupon_start_date = request.POST.get('start_date')
        edit_coupon_end_date = request.POST.get('end_date')
        edit_coupon_is_active = request.POST.get('is_active')
        edit_coupon_applicable_type = request.POST.get('applicable_type')
        edit_coupon_category_id = request.POST.get('category')
        edit_coupon_min_amount = request.POST.get('min_amount')
        edit_coupon_max_amount = request.POST.get('max_amount')

        coupon = Coupon.objects.get(id=coupon_id)

        coupon.name = edit_coupon_name
        coupon.code = edit_coupon_code
        coupon.description = edit_coupon_description
        coupon.discount_type = edit_coupon_discount_type
        coupon.discount = edit_coupon_discount
        coupon.start_date = edit_coupon_start_date
        coupon.end_date = edit_coupon_end_date
        coupon.is_active = bool(edit_coupon_is_active)  # Convert 'true'/'false' to boolean.
        coupon.applicable_type = edit_coupon_applicable_type
        coupon.category_id = edit_coupon_category_id
        coupon.min_purchase = edit_coupon_min_amount
        coupon.max_amount = edit_coupon_max_amount
        coupon.save()
        return redirect('coupon_list')
    return render(request, "admintemp/coupontable.html.html")



def view_coupon(request):
    coupon_view = Coupon.objects.all()
    return render(request, "admintemp/coupontable.html.html")



3