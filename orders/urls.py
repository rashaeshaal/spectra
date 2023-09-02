from orders import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    
    

path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
path('payment_success',views.payment_success, name='payment_success'),


     
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
