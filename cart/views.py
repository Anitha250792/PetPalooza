from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem, Product, Order
import razorpay
from .models import Service
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# ---------------- CART ---------------- #

def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')

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


# ---------------- CHECKOUT ---------------- #

def checkout_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)

    if not items:
        return redirect("cart_page")

    subtotal = sum([item.subtotal() for item in items])
    shipping = 99 if subtotal > 0 else 0
    total = subtotal + shipping

    # 1️⃣ Create Order in DB
    order = Order.objects.create(
        user=request.user,
        total_amount=total,
        is_paid=False
    )

    # 2️⃣ Create Razorpay order
    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    razorpay_order = client.order.create({
        "amount": int(total * 100),   # in paise
        "currency": "INR",
        "receipt": str(order.id),
        "payment_capture": "1"
    })

    # 3️⃣ Save razorpay order id
    order.razorpay_order_id = razorpay_order["id"]
    order.save()

    return render(request, "checkout.html", {
        "items": items,
        "subtotal": subtotal,
        "shipping": shipping,
        "total": total,
        "amount_paise": int(total * 100),
        "razorpay_order_id": razorpay_order["id"],
        "razorpay_key": settings.RAZORPAY_KEY_ID,
    })


# ---------------- PAYMENT SUCCESS ---------------- #

@csrf_exempt
def payment_success(request):

    if request.method != "POST":
        return redirect("home")

    razorpay_order_id = request.POST.get("razorpay_order_id")
    razorpay_payment_id = request.POST.get("razorpay_payment_id")
    razorpay_signature = request.POST.get("razorpay_signature")

    # Billing details
    name = request.POST.get("name")
    address = request.POST.get("address")
    phone = request.POST.get("phone")
    email = request.POST.get("email")

    order = Order.objects.filter(
        razorpay_order_id=razorpay_order_id
    ).first()

    if not order:
        return JsonResponse({"error": "Order not found in database"})

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    try:
        client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        })

        # Save payment details
        order.razorpay_payment_id = razorpay_payment_id
        order.razorpay_signature = razorpay_signature
        order.is_paid = True

        # Save billing details
        order.name = name
        order.address = address
        order.phone = phone
        order.email = email

        order.save()

        # Clear cart
        CartItem.objects.filter(cart__user=request.user).delete()

        return redirect("thankyou", order_id=order.id)

    except:
        return JsonResponse({"error": "Payment verification failed"})

# ---------------- THANK YOU ---------------- #

def thankyou(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "thankyou.html", {"order": order})

def add_to_cart(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    cart = request.session.get('cart', {})

    if str(service_id) in cart:
        cart[str(service_id)]['quantity'] += 1
    else:
        cart[str(service_id)] = {
            'name': service.name,
            'price': float(service.offer_price),
            'quantity': 1
        }

    request.session['cart'] = cart
    return redirect('consult_now')