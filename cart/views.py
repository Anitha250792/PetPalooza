from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem, Product, Order
import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


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

def checkout_view(request):

    if not request.user.is_authenticated:
        return redirect('login')

    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)

    subtotal = sum([item.subtotal() for item in items])
    shipping = 99 if subtotal > 0 else 0
    total = subtotal + shipping

    print("KEY:", settings.RAZORPAY_KEY_ID)
    print("SECRET:", settings.RAZORPAY_KEY_SECRET)


    # Create Razorpay order
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    razorpay_order = client.order.create({
        "amount": int(total * 100),
        "currency": "INR",
        "payment_capture": "1"
    })

    return render(request, "checkout.html", {
        "items": items,
        "subtotal": subtotal,
        "shipping": shipping,
        "total": total,
        "razorpay_order_id": razorpay_order["id"],
        "razorpay_key": settings.RAZORPAY_KEY_ID,
    })

def thankyou(request):
    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        email = request.POST.get("email")

        context = {
            "name": name,
            "address": address,
            "phone": phone,
            "email": email,
        }

        return render(request, "thankyou.html", context)

    return redirect("home")


@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        data = request.POST

        razorpay_order_id = data.get("razorpay_order_id")
        razorpay_payment_id = data.get("razorpay_payment_id")
        razorpay_signature = data.get("razorpay_signature")

        print("Razorpay order id received:", razorpay_order_id)
        print("Orders in DB:", list(Order.objects.values_list("razorpay_order_id", flat=True)))

        order = Order.objects.filter(razorpay_order_id=razorpay_order_id).first()

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

            order.razorpay_payment_id = razorpay_payment_id
            order.razorpay_signature = razorpay_signature
            order.is_paid = True
            order.save()

            # Clear cart
            CartItem.objects.filter(cart__user=request.user).delete()

            return redirect("thankyou", order_id=order.id)

        except:
            return JsonResponse({"error": "Payment verification failed"})




   