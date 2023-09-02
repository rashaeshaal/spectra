from django.shortcuts import render,redirect
from .models import Order
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


# Create your views here.






    
def cancel_order(request, order_id):
    # Retrieve the order object
    order = get_object_or_404(Order, pk=order_id)

    # Check if the order is not already cancelled
    if order.status != "Cancelled":
        # Update the order status to "Cancelled"
        order.status = "Cancelled"
        order.save()
        # Redirect to the order detail page with a success message
        return redirect('view_order', order_id=order_id)
    else:
        # Redirect to the order detail page with an error message
        return redirect('view_order', order_id=order_id, error_message="Order is already cancelled.")


@csrf_exempt
def payment_success(request):
    
    orders=Order.objects.all()
    
    context = {
        'orders' : orders,
    }
    return render(request, 'payment_success.html',context)



