from django.urls import path
from . import views

app_name = "shop"
urlpatterns = [
    path("", views.catalog, name="catalog"),
    path("product/<slug:slug>/", views.product_detail, name="product"),
    path("cart/", views.cart, name="cart"),
    path("cart/add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("cart/update/<int:product_id>/", views.cart_update, name="cart_update"),
    path("checkout/", views.checkout, name="checkout"),
    path("thanks/<int:order_id>/", views.thanks, name="thanks"),
]
