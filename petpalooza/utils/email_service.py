from django.core.mail import send_mail
from django.conf import settings


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


def send_order_confirmation(order):

    items = order.items.all()

    product_lines = ""
    subtotal = 0

    for item in items:

        if item.product:
            name = item.product.name
        else:
            name = item.service.name

        price = item.price
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

PetPalooza Team
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
A new order has been placed.

Customer: {order.name}
Email: {order.email}
Phone: {order.phone}

Order ID: {order.id}
Total Amount: ₹{order.total_amount}

Address:
{order.address}
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        ["ntanithasaravanan@gmail.com"],
        fail_silently=False,
    )