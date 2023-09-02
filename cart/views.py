from django.shortcuts import render,redirect
from adminapp.models import Products
from django.shortcuts import render, get_object_or_404
from .models import CartItem,whishlist
from .forms import CartItemForm
from .models import Cart,Address
from orders.models import Order,OrderItem
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .forms import BillingDetailsForm
from django.contrib import messages
from coupon.models import Coupon,Discount
from orders.models import Orders
import uuid
import razorpay
from spectra.settings import RAZORPAY_KEY_ID,RAZORPAY_KEY_SECRET
from django.db import transaction
client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
from spectra import settings


RAZORPAY_KEY_ID = 'rzp_test_9c9ABO7tWn2Uud'
RAZORPAY_KEY_SECRET = 'tLlzIEgqT1m6K7gf5Q1HXwGN'
from django.http import JsonResponse
from orders.constants import PaymentStatus
import json
from django.views.decorators.csrf import csrf_exempt
import logging
from spectra.settings import (
    RAZORPAY_KEY_ID,
    RAZORPAY_KEY_SECRET,
)






@login_required(login_url='handlelogin')
def wishlist(request):
    print("33333333333333333333")
    try:
        wishlists = whishlist.objects.filter(user=request.user)
        print(wishlist,"444444444444444")
        print(whishlist.product,"555555555555")
    except ObjectDoesNotExist:
        wishlists = []
        

    context = {
        'wishlists': wishlists,
    }
    
    return render(request, "whishlist.html", context)






def add_to_wishlist(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    
    existing_wishlist = whishlist.objects.filter(product=product, user=request.user).exists()
    if not existing_wishlist:
        wishlist = whishlist.objects.create(
            product=product,
            user=request.user
        )
        return redirect('wishlist')  # Redirect to the wishlist page after successful addition
    else:
        print("Product already exists in the wishlist.")
        return redirect('wishlist')  # Redirect to the wishlist page even if the product exists

    
def remove_wishlist(request, product_id):
    try:
        wishlist_items = whishlist.objects.filter(user=request.user, product_id=product_id)
        for wishlist_item in wishlist_items:
            wishlist_item.delete()
    except whishlist.DoesNotExist:
        # Handle the case where the wishlist item does not exist
        pass
    return redirect('wishlist')
    
 






def update_cart(request):
    if request.method == "POST" and request.is_ajax():
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity")

        # Update the cart in your database with the new quantity
        # ... Your code here ...

        # Return a JSON response to acknowledge the update
        # return JsonResponse({"success": True})

    # If the request is not a POST or not AJAX, return an error response
    return JsonResponse({"error": "Invalid request"})


# def cartpage(request):
#     total = 0
#     quantity = 0
#     cart_items = None
#     grand_total = 0
#     total_discount = 0 
#     coupons = []
    
#     try:
#         cart = Cart.objects.get(cart_id=_cart_id(request))
#         cart_items = CartItem.objects.filter(cart=cart, is_active=True)
#         for cart_item in cart_items:
#             total += (cart_item.product.product_price * cart_item.quantity)  # Access the product price
#             quantity += cart_item.quantity
            
            
#         grand_total = total
#         for coupon in coupons:
#             total_discount += coupon.discount
        
#         coupons = Coupon.objects.filter(is_active = True )
#     except Cart.DoesNotExist:
#         pass
    
#     context = {
#         'total': total,
#         'quantity': quantity,
#         'cart_items': cart_items,
#         'grand_total': grand_total,
#         'total_discount': total_discount,
#         "coupons":coupons,
#     }
    
#     return render(request, "cart.html", context)

def cartpage(request):
    total = 0
    quantity = 0
    cart_items = None
    grand_total = 0
    total_discount = 0
    coupons = []

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.product_price * cart_item.quantity)  # Access the product price
            quantity += cart_item.quantity

       
        
        for coupon in coupons:
            total_discount += coupon.discount
            coupons = Coupon.objects.filter(is_active=True)
       
        total -= total_discount
        print('wwwwwwwwwwwwwwwww')
        # Calculate the total discount based on applied coupons

        # Save the total discount in the database
        discount = Discount(total_discount=total_discount)
        discount.save()
        

    except Cart.DoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'grand_total': grand_total,
        'total_discount': total_discount,  # Pass the total_discount to the context
        "coupons": coupons,
    }

    return render(request, "cart.html", context)

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart




@login_required(login_url='handlelogin')
def checkoutpage(request):
    current_user = request.user
    cart = Cart.objects.filter(cartitem__user=current_user).first()
    if not cart:
        return redirect('home')

    cart_items = cart.cartitem_set.all()
    coupon_price = cart.coupon.discount
   
   
    total = cart.total()
    discount_price = total - coupon_price
    
    
   

    billing_info = None
    total_discount = 0 
    # total = 0
    # coupons = []
    
   
   
    # for coupon in coupons:
    #     total_discount += coupon.discount
    #     coupons = Coupon.objects.filter(is_active=True)
  
    # total -= total_discount

   

    

    if request.method == 'POST':
        form = BillingDetailsForm(request.POST)
        if form.is_valid():
            billing_info = form.save(commit=False)
            billing_info.user = current_user
            billing_info.save()
           

            with transaction.atomic():
                order = Order.objects.create(
                    user=current_user,
                    address=billing_info,
                    total_amount=total,
                    payment_mode=False,  # Initialize as False, assuming default is not COD
                    status='pending',
                )

                # Create OrderItems for each cart item
                for cart_item in cart_items:
                    order_item = OrderItem.objects.create(
                        order_no=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        product_price=cart_item.product.product_price,
                    )
                    order_item.save()
                    cart_items.delete()

                # Process Payment Method
              
                    

                # ... rest of your code ...
           

    else:
        form = BillingDetailsForm()

    context = {
        'cart_items': cart_items,
        'total': total,
        'form': form,
        'billing_info': billing_info,
        'discount_price':discount_price,
        
        
        
        # "coupons":coupons,
       
        
        
    }
    return render(request, 'checkout.html', context)



def singleproduct(request, product_id):
    single_product = get_object_or_404(Products, pk=product_id)
    in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    
    
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    return render(request,"singlepd.html",context)
     
def add_cart(request, product_id):
    product = Products.objects.get(id=product_id)
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        if request.user.is_authenticated:
            if product.offer_price is not None:
                total_price = product.offer_price
            else:
                total_price = product.product_price

            cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart, user=request.user)
        else:
            if product.offer_price is not None:
                total_price = product.offer_price
            else:
                total_price = product.product_price

            cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
    
    return redirect('cartpage')

       
def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Products, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)

    # Set the quantity to 0 to remove the item from the cart
    cart_item.quantity = 0
    cart_item.save()

    return redirect('cartpage')


def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Products, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cartpage')

def increase_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cartpage')

def decrease_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cartpage')

def place_order(request):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart = Cart.objects.filter(cartitem__user=current_user).first()
    cart_count = cart_items.count()
    print('nnnnnnnnnnn')

    if cart_count <= 0:
        return redirect('payment_success')
    

    total = 0
    for cart_item in cart_items:
        total += cart_item.product.product_price * cart_item.quantity
         # Calculate total discount
   
    coupon_price = cart.coupon.discount
    # Calculate final total after applying discount
    discount_price = total - coupon_price
    
    
    

    if request.method == 'POST':
        form = BillingDetailsForm(request.POST)
        if form.is_valid():
            billing_info = form.save(commit=False)
            billing_info.user = current_user
            billing_info.save()
            print('gggggggggggg')

            # Create the order instance
            order = Order.objects.create(
                user=current_user,
                address=billing_info,
                total_amount=discount_price,
                payment_mode=True,
                status='pending',
            )

            for cart_item in cart_items:
                order_item = OrderItem.objects.create(
                    order_no=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    product_price=cart_item.product.product_price,  # Add product price
                )
                order_item.save()

            cart_items.delete()

            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(order.id)
            order.order_number = order_number
            order.save()

            messages.success(request, f'Order placed successfully. Your order number is: {order_number}')
            
            payment_method = request.POST.get('payment_mode')
            print(payment_method,'hhhhhhhhhh')
            if payment_method == 'cod':
                print('rrrrrrrr')
                order.payment_mode = 'True' 
                # order.payment_mode = False
                order.payment_method = 'COD'
             
                order.save()
            elif payment_method == 'razorpay':
                print("jjjjjjjjjj")

                order.payment_mode = 'True'  # Set Razorpay flag to True
                order.payment_method = 'Razorpay'
                order.save()
            
            if payment_method == 'cod':
                print("aaaaaaaaaaaaaaa")
                return redirect('payment_success')  # Redirect for COD
            elif payment_method == 'razorpay':
                amount = str(discount_price)
                name = current_user.first_name,
                amount = float(amount)
                client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
                razorpay_order = client.order.create(
                    {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
                    )
                order = Orders.objects.create(
                    name=current_user.first_name, amount=amount, provider_order_id=razorpay_order["id"]
                    )
                order.save()
                return render(request,"payment.html",
                              {
                                  "callback_url": "http://" + "127.0.0.1:8000" + "/cart/callback/",
                                  "razorpay_key": RAZORPAY_KEY_ID,
                                  "order": order,
                                  },
                              )
                return render(request, "payment.html")

        else:
            print("Form is invalid. Errors:", form.errors)
            messages.error(request, 'Invalid form data. Please check your input.')
            return redirect('checkoutpage')
    else:
        form = BillingDetailsForm()

    context = {
        'cart_items': cart_items,
        'total': total,
        'form': form,
        # 'total_discount': total_discount,
        # "coupons":coupons,
        
        
    }
    return render(request, "checkout.html", context)
    
@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)
        print('11111111111111111111111111111')
    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        print("Provider Order ID:", provider_order_id)
        signature_id = request.POST.get("razorpay_signature", "")
        order = Orders.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        if verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()
            return render(request, "payment_success.html", context={"status": order.status})
        else:
            order.status = PaymentStatus.FAILURE
            order.save()
            return render(request, "payment_success.html", context={"status": order.status})
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Orders.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "payment_success.html", context={"status": order.status})


def payment_success(request):
    return render(request, "payment_success.html")
    
    





def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        print(coupon_code,'vvvvvvvvvvvvvvvvvvvvvvvv')
        try:
            coupon = Coupon.objects.get(code=coupon_code, is_active=True)
            # Apply coupon discount to grand total
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            total = 0
            for cart_item in cart_items:
                total += (cart_item.product.product_price * cart_item.quantity)
            coupon_discount = coupon.discount  # Store the coupon discount amount
            grand_total = total - coupon.discount  # Update grand total with coupon discount
            cart.grand_total = grand_total
            cart.coupon = coupon
            
            cart.save()
            # try:
            #     if coupon_code:
            #         cart.coupon=coupon.id
            #         cart.save()
            # except:
            #     pass
            
            # Return coupon discount and updated grand total in the JSON response
            response_data = {
                'success': True,
                'coupon_discount': coupon_discount,
                'grand_total': grand_total
            }
            
            return JsonResponse(response_data)
        except Coupon.DoesNotExist:
            messages.error(request, 'Invalid coupon code.')
        return redirect('cartpage')

