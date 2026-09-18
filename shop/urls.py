from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="product_list"),

    path(
        "product/<int:product_id>/",
        views.product_detail,
        name="product_detail"
    ),

    path(
        "cart/add/<int:product_id>/",
        views.add_to_cart,
        name="add_to_cart"
    ),

    path(
        "cart/",
        views.cart_view,
        name="cart"
    ),

    path(
        "register/",
        views.register_view,
        name="register"
    ),

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    path(
        "checkout/",
        views.checkout_view,
        name="checkout"
    ),

    path(
        "orders/",
        views.order_history,
        name="order_history"
    ),

    path(
        "orders/<int:order_id>/",
        views.order_detail,
        name="order_detail"
    ),
]