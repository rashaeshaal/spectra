from cart import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
  
path('cartpage',views.cartpage,name="cartpage"), 
path('checkoutpage',views.checkoutpage,name="checkoutpage"),
path('singleproduct/<int:product_id>/', views.singleproduct, name='singleproduct'),
path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'), 
path('remove_cart/<int:product_id>/<int:cart_item_id>', views.remove_cart, name='remove_cart'), 
path('remove_cart_item/<int:product_id>/', views.remove_cart_item, name='remove_cart_item'),
path('increase_quantity/<int:cart_item_id>/', views.increase_quantity, name='increase_quantity'),
path('decrease_quantity/<int:cart_item_id>/', views.decrease_quantity, name='decrease_quantity'),
path('place_order/', views.place_order, name='place_order'),
path('update_cart/', views.update_cart, name='update_cart'),
path('wishlist',views.wishlist,name="wishlist"), 
path('add_to_wishlist/<int:product_id>/',views.add_to_wishlist, name="add_to_wishlist"),
path('remove_wishlist/<int:product_id>/', views.remove_wishlist, name='remove_wishlist'),
path('apply_coupon',views.apply_coupon, name='apply_coupon'),
path('callback/', views.callback, name='callback'),
path('payment_success',views.payment_success, name='payment_success'),

]   
    
    


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
