from accounts import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('index/',views.index,name="home"),
    path('signup/',views.signup,name="signup"),
    path('otp/',views.verify_otp,name="verifyotp"),
    path('handlelogin/',views.handlelogin,name="handlelogin"),
    path('logout/',views.handlelogout,name="handlelogout"),
    path('productpage/',views.productpage,name="productpage"),
   
    path('reset_password', views.reset_password, name='reset_password'),
    path('confirm_reset_password/<uidb64>/<token>/', views.confirm_reset_password, name='confirm_reset_password'),
    path('profile_view/', views.profile_view, name='profile_view'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('userorder/', views.userorder, name='userorder'),
    path('view_order/<int:order_id>/', views.view_order, name='view_order'),
    path('manage_addresses/', views.manage_addresses, name='manage_addresses'),
    path('delete_address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('edit_address/<int:address_id>/', views.edit_address, name='edit_address'),
    path('add_address/', views.add_address, name='add_address'),
    # path('cancel_order/', views.cancel_order, name='cancel_order'),
   
    
   

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)