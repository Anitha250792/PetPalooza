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
    subject = "PetPalooza Order Confirmation"

    message = f"""
Hello {order.name},

Your payment was successful.

Order ID: {order.id}
Total Amount: ₹{order.total_amount}

Delivery Address:
{order.address}

Thank you for shopping with PetPalooza.

– PetPalooza Team
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