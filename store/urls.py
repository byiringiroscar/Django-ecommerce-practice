from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="updateItem"),  # here we could have used csrf_exempt(
    # views.updateItem) in order to avoid csrf 404 forbidden but we are going to replicate by using csrftoken from
    # django doc link https://docs.djangoproject.com/en/3.2/ref/csrf/   we are going to paste the code in main.html
    path('process_order/', views.processOrder, name="processOrder"),
    # path('product/<str:pk>/', views.product, name="product"), # this is for testing if we can run user by using device id
    path('product_ajx/<str:pk>/', views.product_ajx, name="product_ajx"),
    path('add-to-cart-ajax', views.add_to_cart_ajax, name="add-to-cart-ajax"),
    path('list-cart-ajax/', views.list_cart_ajax, name="list-cart-ajax"),
    path('delete-from-cart-ajax', views.delete_from_cart_ajax, name="delete-from-cart-ajax"),
    path('update-from-cart-ajax', views.update_from_cart_ajax, name="update_from_cart_ajax"),
    path('new-store-ajax/', views.new_store_ajax, name="new_store_ajax", )

]
