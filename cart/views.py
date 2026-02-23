from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem, Product
import razorpay
from django.conf import settings
from django.http import JsonResponse


def add_to_cart(request, product_id):

    if not request.user.is_authenticated:
        return redirect('login')

    # safer than Product.objects.get()
    product = get_object_or_404(Product, id=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect('cart_page')

def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart_page')


def increase_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.quantity += 1
    item.save()
    return redirect('cart_page')


def remove_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart_page')




def cart_page(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)

    subtotal = sum([item.subtotal() for item in items])
    shipping = 99 if subtotal > 0 else 0
    total = subtotal + shipping

    return render(request, 'addtocart.html', {
        'items': items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total
    })

def checkout_page(request):

    if not request.user.is_authenticated:
        return redirect('login')

    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)

    subtotal = sum([item.subtotal() for item in items])
    shipping = 99 if subtotal > 0 else 0
    total = subtotal + shipping

    return render(request, "checkout.html", {
        "items": items,
        "subtotal": subtotal,
        "shipping": shipping,
        "total": total,
    })

def checkout_view(request):
    items = ...
    subtotal = ...
    shipping = ...
    total = subtotal + shipping

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    razorpay_order = client.order.create({
        "amount": int(total * 100),  # amount in paisa
        "currency": "INR",
        "payment_capture": "1"
    })

    context = {
        "items": items,
        "subtotal": subtotal,
        "shipping": shipping,
        "total": total,
        "razorpay_order_id": razorpay_order["id"],
        "razorpay_key": settings.RAZORPAY_KEY_ID,
    }

    return render(request, "checkout.html", context)

def thankyou(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "thankyou.html", {"order": order})
   