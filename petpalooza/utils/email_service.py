from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


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

    rows = ""
    subtotal = 0

    for item in items:

        if item.product:
            name = item.product.name
        else:
            name = item.service.name

        price = item.price
        qty = item.quantity
        total = price * qty

        subtotal += total

        rows += f"""
        <tr>
            <td>{name}</td>
            <td>{qty}</td>
            <td>₹{price}</td>
            <td>₹{total}</td>
        </tr>
        """

    shipping = 99 if subtotal > 0 else 0
    grand_total = subtotal + shipping

    subject = f"PetPalooza Order Confirmation - #{order.id}"

    html_message = f"""
    <html>
    <body style="font-family:Arial;background:#f6f6f6;padding:20px;">

        <div style="max-width:600px;background:white;margin:auto;padding:20px;border-radius:10px;">

            <h2 style="color:#1f4df0;">🐾 PetPalooza</h2>

            <h3>Order Confirmation</h3>

            <p>Hello {order.name},</p>

            <p>Thank you for your purchase!</p>

            <p><b>Order ID:</b> {order.id}</p>

            <table border="1" cellpadding="10" cellspacing="0" width="100%" style="border-collapse:collapse">

                <tr style="background:#f2f2f2;">
                    <th>Product</th>
                    <th>Qty</th>
                    <th>Price</th>
                    <th>Total</th>
                </tr>

                {rows}

            </table>

            <br>

            <p><b>Subtotal:</b> ₹{subtotal}</p>
            <p><b>Shipping:</b> ₹{shipping}</p>

            <h3>Total Paid: ₹{grand_total}</h3>

            <hr>

            <p><b>Delivery Address</b></p>
            <p>{order.address}</p>

            <p style="color:gray;">Thank you for shopping with PetPalooza.</p>

        </div>

    </body>
    </html>
    """

    email = EmailMultiAlternatives(
        subject,
        "",
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
    )

    email.attach_alternative(html_message, "text/html")
    email.send()


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