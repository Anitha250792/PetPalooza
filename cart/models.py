from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


# ---------------- PRODUCTS ---------------- #

class Product(models.Model):

    name = models.CharField(max_length=200)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    image = CloudinaryField('image', blank=True, null=True)

    weight = models.CharField(max_length=50, blank=True, null=True)

    category = models.CharField(max_length=100, blank=True, null=True)

    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)

    review_count = models.IntegerField(default=0)

    @property
    def rating_int(self):
        return int(self.rating)

    def __str__(self):
        return self.name


# ---------------- SERVICES ---------------- #

class Service(models.Model):

    name = models.CharField(max_length=200)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    offer_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


# ---------------- CART ---------------- #

class Cart(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} Cart"


class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    quantity = models.IntegerField(default=1)

    def subtotal(self):

        if self.product:
            return self.product.price * self.quantity

        if self.service:
            return self.service.offer_price * self.quantity

        return 0

    def __str__(self):

        if self.product:
            return f"{self.product.name} ({self.quantity})"

        if self.service:
            return f"{self.service.name} ({self.quantity})"

        return "Cart Item"


# ---------------- ORDER ---------------- #

class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    razorpay_order_id = models.CharField(max_length=200)

    razorpay_payment_id = models.CharField(max_length=200, blank=True, null=True)

    razorpay_signature = models.CharField(max_length=500, blank=True, null=True)

    name = models.CharField(max_length=200, blank=True, null=True)

    email = models.EmailField(blank=True, null=True)

    phone = models.CharField(max_length=20, blank=True, null=True)

    address = models.TextField(blank=True, null=True)

    # 🚚 SHIPPING INFORMATION
    tracking_id = models.CharField(max_length=200, blank=True, null=True)
    courier_name = models.CharField(max_length=200, blank=True, null=True)

    estimated_delivery = models.DateField(blank=True, null=True)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    is_paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


# ---------------- ORDER ITEMS ---------------- #

class OrderItem(models.Model):

    STATUS_CHOICES = [
        ("Order Placed", "Order Placed"),
        ("Packed", "Packed"),
        ("Shipped", "Shipped"),
        ("Out for Delivery", "Out for Delivery"),
        ("Delivered", "Delivered"),
    ]

    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    quantity = models.IntegerField(default=1)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="Order Placed",
        db_index=True
    )

    current_location = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)

    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        item_name = self.product.name if self.product else (
            self.service.name if self.service else "Order Item"
        )
        return f"{item_name} ({self.quantity})"