from django.core.mail import send_mail
from django.conf import settings
from cart.models import CartItem


def send_welcome_email(user):
    subject = "Welcome to PetPalooza 🐾"
    message = f"""
Hi {user.first_name},

Welcome to PetPalooza!

Your account has been successfully created.

You can now:
• Book pet consultations
• Purchase pet products
• Explore our services

Thank you for joining us.

– PetPalooza Team
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )


from django.core.mail import send_mail
from django.conf import settings
from cart.models import CartItem


def send_order_confirmation(order):

    items = CartItem.objects.filter(cart__user=order.user)

    product_lines = ""
    subtotal = 0

    for item in items:
        if item.product:
            name = item.product.name
            price = item.product.price
        elif item.service:
            name = item.service.name
            price = item.service.offer_price
        else:
            continue

        quantity = item.quantity
        line_total = price * quantity
        subtotal += line_total

        product_lines += f"""
{name}
Qty: {quantity}
Price: ₹{price}
Total: ₹{line_total}

"""

    shipping = 99 if subtotal > 0 else 0
    grand_total = subtotal + shipping

    subject = f"PetPalooza Order Confirmation - Order #{order.id}"

    message = f"""
Hello {order.name},

Thank you for your order!

Order ID: {order.id}

-----------------------------
ORDER SUMMARY
-----------------------------

{product_lines}

Subtotal: ₹{subtotal}
Shipping: ₹{shipping}

Total Paid: ₹{grand_total}

-----------------------------

Delivery Address:
{order.address}

We will process your order shortly.

Thank you for shopping with PetPalooza!

PetPalooza Team
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
        fail_silently=False,
    )


def send_consultation_confirmation(email, name):
    subject = "Pet Consultation Booking Confirmed"

    message = f"""
Hello {name},

Your pet consultation request has been received.

Our expert will contact you soon.

Thank you for choosing PetPalooza.

– PetPalooza Team
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )

def send_admin_order_notification(order):
    subject = f"New Order Received - Order #{order.id}"

    message = f"""
A new order has been placed on PetPalooza.

Customer Name: {order.name}
Email: {order.email}
Phone: {order.phone}

Order ID: {order.id}
Total Amount: ₹{order.total_amount}

Shipping Address:
{order.address}

Check admin dashboard for more details.
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        ["ntanithasaravanan@gmail.com"],  # admin email
        fail_silently=False,
    )    