from adminapp import views
from django.urls import path
from .views import add_category
from django.conf.urls.static import static


urlpatterns = [
     path('admin_dashboard/',views.admin_dashboard,name="admin_dashboard"),
     path('categorylist/',views.categorylist,name="categorylist"),
     path('productlist/',views.productlist,name="productlist"),
     path('add_category/',views.add_category, name='add_category'),
     path('admins/edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
     path('admin_login/',views.admin_signin, name='admin_login'),
     path('admin_logout/',views.admin_logout, name='admin_logout'),
     path('admins/add_product/', views.add_product, name='add_product'),
     path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
     path('user_details/',views.user_details,name="user_details"),
     path('user_block/<int:user_id>/',views.user_block,name='user_block'),
     path('user_unblock/<int:user_id>/',views.user_unblock,name="user_unblock"),
     path('brands/', views.brandslist, name="brandslist"),
     path('add_brand/', views.add_brand, name="add_brand"),
     path('orderdetails/', views.orderdetails, name="orderdetails"),
     path('edit_brand/<int:brand_id/',views.edit_brand,name="edit_brand"),
     path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
     path('manage_order', views.manage_order, name='manage_order'),
     path('manage_orderstatus/<int:order_id>/', views.manage_orderstatus, name='manage_orderstatus'),
     path('product_block/<int:id>/', views.product_block, name='product_block'),
     path('product_unblock/<int:id>/', views.product_unblock, name='product_unblock'),
     path('admins/edit_product/<int:id>/', views.edit_product, name='edit_product'),
     path('admin/coupon/list/', views.coupon_list, name='coupon_list'),
     path('admin/coupon/add/', views.add_coupon, name='add_coupon'),
     path('admin/coupon/edit/<int:coupon_id>/', views.edit_coupon, name='edit_coupon'),
     path('admin/coupon/view/', views.view_coupon, name='view_coupon'),
     path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
     path('order/delete/<int:order_id>/', views.delete_order, name='delete_order'),
     path('sales_report', views.sales_report, name='sales_report'),
     path('admin_signin', views.admin_signin, name='admin_signin'),
     path('orderview/<int:order_id>/', views.orderview, name='orderview'),
     path('product_gallery_list/', views.product_gallery_list, name='product_gallery_list'),
     path('edit_gallery/<int:product_id>/', views.edit_gallery, name='edit_gallery'),
     # path('delete_gallery/<int:product_id>/<int:image_id>/', views.delete_gallery, name='delete_gallery'),
     path('add_gallery/', views.add_gallery, name='add_gallery'),
     # path('delete_image/<int:image_id>/', views.delete_image, name='delete_image'),
     path('admins/delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
     path('admins/delete_image/<int:image_id>/', views.delete_image, name='delete_image'),




     
]


     
     
     
     

     
    



