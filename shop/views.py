from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import (
    Product,
    Cart,
    CartItem,
    Order,
    OrderItem,
)


# -------------------------
# PRODUCT LIST
# -------------------------
def product_list(request):
    products = Product.objects.filter(available=True)

    return render(
        request,
        "shop/product_list.html",
        {"products": products}
    )


# -------------------------
# PRODUCT DETAIL
# -------------------------
def product_detail(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
        available=True
    )

    return render(
        request,
        "shop/product_detail.html",
        {"product": product}
    )


# -------------------------
# ADD TO CART
# -------------------------
def add_to_cart(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
        available=True
    )

    if not request.user.is_authenticated:
        return redirect("login")

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1

    cart_item.save()

    return redirect("cart")


# -------------------------
# CART
# -------------------------
def cart_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    items = cart.items.all()

    total = sum(
        item.total_price()
        for item in items
    )

    return render(
        request,
        "shop/cart.html",
        {
            "cart": cart,
            "items": items,
            "total": total,
        }
    )


# -------------------------
# REGISTER
# -------------------------
def register_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(
            username=username
        ).exists():

            return render(
                request,
                "shop/register.html",
                {
                    "error": "Username already exists."
                }
            )

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect("login")

    return render(
        request,
        "shop/register.html"
    )


# -------------------------
# LOGIN
# -------------------------
def login_view(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("product_list")

        return render(
            request,
            "shop/login.html",
            {
                "error": "Invalid username or password."
            }
        )

    return render(
        request,
        "shop/login.html"
    )


# -------------------------
# LOGOUT
# -------------------------
def logout_view(request):

    logout(request)

    return redirect("product_list")


# -------------------------
# CHECKOUT
# -------------------------
def checkout_view(request):

    if not request.user.is_authenticated:
        return redirect("login")

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    items = cart.items.all()

    if not items:
        return redirect("cart")

    total = sum(
        item.total_price()
        for item in items
    )

    if request.method == "POST":

        shipping_address = request.POST[
            "shipping_address"
        ]

        payment_method = request.POST[
            "payment_method"
        ]

        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            payment_method=payment_method,
            total_amount=total
        )

        for item in items:

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        items.delete()

        return redirect("order_history")

    return render(
        request,
        "shop/checkout.html",
        {
            "items": items,
            "total": total,
        }
    )


# -------------------------
# ORDER HISTORY
# -------------------------
def order_history(request):

    if not request.user.is_authenticated:
        return redirect("login")

    orders = request.user.orders.all().order_by(
        "-created_at"
    )

    return render(
        request,
        "shop/order_history.html",
        {
            "orders": orders
        }
    )
def order_detail(request, order_id):

    if not request.user.is_authenticated:
        return redirect("login")

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    items = order.items.all()

    return render(
        request,
        "shop/order_detail.html",
        {
            "order": order,
            "items": items
        }
    )