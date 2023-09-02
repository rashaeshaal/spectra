from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from userapp.views import index
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate ,login ,logout
from django.http import HttpResponse
from .models import CustomUser,UserProfile
from .models import UserProfile

from django.shortcuts import render, get_object_or_404
from django.utils import timezone,datetime_safe
from django.core.mail import send_mail
from django.conf import settings
import random
from django.contrib.auth.decorators import login_required
from adminapp.models import Products,Category
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from .forms import UserForm,UserProfileForm
from orders.models import Order,OrderItem
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import update_session_auth_hash
import os


# Create 

def index(request):
    return render(request,"index.html")

# def productpage(request):
#     products=Products.objects.filter(product_status=True)
#     all_categories = Category.objects.all()
#     selected_categories = request.GET.getlist('category')
#     min_price = request.GET.get('price_from')
#     max_price = request.GET.get('price_to')

#     if selected_categories:
#         selected_category_ids = Category.objects.filter(name__in= selected_categories).values_list('id', flat=True)
#         products = products.filter(product_category__in= selected_category_ids)

#     if min_price and max_price:
#         products = products.filter(product_price__gte=min_price, product_price__lte=max_price)

#     product_count = products.count()
#     for product in products:
#         print(product.product_name,product.product_image,product.product_brand)
#     context = {
#         'products':products,
#         'product_count':product_count,
#         'categories': all_categories,
#     }
#     return render(request,"product.html",context)

def productpage(request):
    products = Products.objects.filter(product_status=True)
    all_categories = Category.objects.all()

    selected_categories = request.GET.getlist('category')
    min_price = request.GET.get('price_from')
    max_price = request.GET.get('price_to')

    # Filter by selected categories
    if selected_categories:
        selected_category_ids = Category.objects.filter(name__in=selected_categories).values_list('id', flat=True)
        products = products.filter(product_category__in=selected_category_ids)

    # Filter by price range
    if min_price and max_price:
        try:
            min_price = float(min_price)
            max_price = float(max_price)
            products = products.filter(product_price__range=(min_price, max_price))
        except ValueError:
            # Handle invalid price inputs here (e.g., non-numeric input)
            pass

    product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
        'categories': all_categories,
    }
    return render(request, "product.html", context)


@never_cache
def signup(request):
    if request.method=="POST":
        print('hiiiiiii')
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST['password']
        password1=request.POST['password1']
        
        
        if password!=password1:
            messages.warning(request,"Password is Not ")
            return redirect(signup)
        if password==password1:
            if CustomUser.objects.filter(email=email).exists() or CustomUser.objects.filter(mobile=phone_number).exists():
                messages.success(request,'Already exist')
                return redirect(handlelogin)
            
            print(password1)
            otp = ''.join(random.choices('0123456789', k=6))
            user = CustomUser.objects.create_user(first_name=first_name,email=email, password=password1, mobile=phone_number, otp=otp, is_active=False) 
            print('data entered without verification')  
            send_mail('Email Verification', f'Your OTP is: {otp}', settings.EMAIL_HOST_USER, [email], fail_silently=False)
            request.session['otp_created_at'] = timezone.now().isoformat()
            
            print('email send')
            return redirect('verifyotp')
    return render(request,"authentication/signup.html")
 

def handlelogin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        userpassword = request.POST.get('password')
        
        try:
            user = CustomUser.objects.get(email=email)
            
            myuser = authenticate(email=email, password=userpassword)

            if myuser is not None:
                login(request, myuser)
                return redirect("home")  # Redirect to the home page after successful login
            else:
                messages.error(request, "Invalid Credentials")
                return redirect("index")
        except CustomUser.DoesNotExist:
            messages.error(request, "User does not exist")
            return redirect("index")
    
    return render(request, "authentication/login.html")

@login_required    
@never_cache
def handlelogout (request):
    logout(request)
    messages.info(request,"logout sucess")
    
    return render(request,"authentication/login.html")
@never_cache
def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        
        try:
            user = CustomUser.objects.get( otp=otp)
            otp_created_at_str = request.session.get('otp_created_at')

            if otp_created_at_str is None:
                return redirect('verifyotp')
            otp_created_at = datetime_safe.datetime.fromisoformat(otp_created_at_str)
            current_time = timezone.now()
            if (current_time - otp_created_at).total_seconds() > 300:
                error_message = 'OTP has expired. Please request a new OTP.'
                return render(request, 'authentication/otppage.html', {'error_message': error_message})
            user.is_active = True
            user.save()

            customers = CustomUser.objects.all()


            request.session.pop('otp_created_at')
            return redirect('handlelogin')
        except CustomUser.DoesNotExist:
            return redirect('verifyotp')
    
    return render(request,'authentication/otppage.html')

# --------------------------Reset password view--------------------------------------------------
User = get_user_model()

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            # Generate password reset token
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            # Build the reset link URL
            reset_url = f"{request.scheme}://{request.get_host()}/authentication/confirm_reset_password/{uid}/{token}/"

            # Send the password reset email
            subject = 'Password Reset'
            message = render_to_string('authentication/reset_password_email.html', {
                'user': user,
                'reset_url': reset_url,
            })
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

            messages.success(request, 'Password reset link sent to your email.')
            return redirect('handlelogin')
        else:
            messages.error(request, 'User with this email does not exist.')
            return redirect('reset_password')

    return render(request, 'authentication/resetPassword.html')


def confirm_reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()  # Decode URLsafe base64 and convert to string
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Password reset successful. You can now log in with your new password.')
                return redirect('handlelogin')
        else:
            form = SetPasswordForm(user)

        return render(request, 'authentication/confirm_reset_password.html', {'form': form})
    else:
        messages.error(request, 'Invalid password reset link. Please try again.')
        return redirect('handlelogin')


@login_required(login_url='handlelogin')
def profile_view(request):
    if request.method == 'POST':
        if 'change_password' in request.POST:
            # Handle password change form submission
            current_password = request.POST.get('current_password')
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')

            user = request.user
            if user.check_password(current_password):
                if new_password1 == new_password2:
                    user.set_password(new_password1)
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, "Password changed successfully.")
                else:
                    messages.error(request, "New passwords do not match.")
            else:
                messages.error(request, "Incorrect current password.")
        else:
            # Handle profile information update form submission
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone_number = request.POST.get('phone_number')

            user = request.user
            user.username = username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.phone_number = phone_number
            user.save()

            messages.success(request, "Profile updated successfully.")
            
        return redirect('profile_view')

    context = {
        'user': request.user,
    }
        
  
    return render(request, 'authentication/profile_view.html',context)

    


@login_required
def edit_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        # Get the form data from the POST request
        profile_pic = request.FILES.get('profile_pic')
        address_line_1 = request.POST.get('address_line_1')
        # Add other form fields here as needed

        # Update the user profile with the new data
        user_profile.profile_pic = profile_pic
        user_profile.address_line_1 = address_line_1
        # Update other profile fields here as needed

        # Save the changes to the user profile
        user_profile.save()

        # After successfully saving the changes, redirect to the profile view
        return redirect('profile_view')

    return render(request, 'authentication/edit_profile.html',{'user_profile': user_profile})


def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'authentication/my_orders.html', context)


def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'authentication/edit_profile.html', context)

# def userorder(request):
#     orders = Order.objects.all()
#     for order in orders:
#         print(order)
#     context = {
#         'orders': orders,
#     }
#     return render(request,'userorder.html',context)

def userorder(request):
    current_user = request.user
    orders = Order.objects.filter(user=current_user)
    
    context = {
        'orders': orders,
    }
    return render(request, 'userorder.html', context)



# def cancel_order(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
    
#     if request.method == 'POST':
#         if 'confirm_cancel' in request.POST:
#             order.cancel_order()
#             return redirect('view_order', order_id=order_id)
    
#     context = {'order': order}
#     return render(request, 'user_order.html', context)
def view_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order_no=order)

    if request.method == 'POST':
        if 'cancel_order' in request.POST:
            order.cancel_order()
            messages.success(request, 'Order has been cancelled successfully.')
            return redirect('order_detail', order_id=order_id)

    context = {'order': order, 'order_items': order_items}
    return render(request, 'user_order.html', context)
# --------------------------manage addresses---------------------------------------

def manage_addresses(request):
    if request.method == 'POST':
        # Handle the form submission to add a new address
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('mobile')
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2', '')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')

        # Create a new Address object and save it to the database
        address = UserProfile(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            city=city,
            state=state,
            postcode=postal_code,
            country=country,
            user=request.user
        )
        address.save()

        # Redirect to the manage addresses page after adding the new address
        return redirect('manage_addresses')

    else:
        # Retrieve the existing addresses for the current user
        addresses = UserProfile.objects.filter(user=request.user)

        context = {
            'addresses': addresses
        }
        return render(request, 'authentication/manage.html', context)

def delete_address(request, address_id):
    try:
        address = UserProfile.objects.get(id=address_id)
        address.delete()
        # You can add a success message here if you want
    except UserProfile.DoesNotExist:
        # Address with the given ID not found, you can handle this error accordingly
        pass
    return redirect('manage_addresses')



def edit_address(request, address_id):
    address = get_object_or_404(UserProfile, id=address_id)
    if request.method == 'POST':
        # Get the updated values from the POST data
        address.first_name = request.POST.get('first_name')
        address.last_name = request.POST.get('last_name')
        address.email = request.POST.get('email')
        address.phone = request.POST.get('mobile')
        address.address_line_1 = request.POST.get('address_line_1')
        address.city = request.POST.get('city')
        address.state = request.POST.get('state')
        address.country = request.POST.get('country')
        address.save()
        # You can add a success message here if you want
        return redirect('manage_addresses')

    context = {
        'address': address,
        'address_id': address_id,
    }
    return render(request, 'authentication/edit_address.html', context)



@login_required(login_url='handlelogin')
def add_address(request):
    # Check if the user already has a UserProfile
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        print('hello')
        # Get the form fields from the POST data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('mobile')
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')
        print("Address saved successfully:", profile)
        print("phone:", phone)
        print("firstname", first_name)

        # Update the UserProfile fields
        profile.first_name = first_name
        profile.last_name = last_name
        profile.email = email
        profile.mobile = phone
        
        profile.address_line_1 = address_line_1
        profile.address_line_2 = address_line_2
        profile.postcode = postal_code
        profile.area = state
        profile.state = state
        profile.country = country

        # Set additional fields on the user model
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email
        request.user.phone = phone

        # Save the changes
        profile.save()
        request.user.save()

        # Redirect back to the manage_addresses page
        return redirect('manage_addresses')

    return render(request, 'authentication/add_address.html', {'profile': profile})
