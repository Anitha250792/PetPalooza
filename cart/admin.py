from django.contrib import admin
from .models import Product, Cart, CartItem, Service, OrderItem, Order


admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Service)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "service", "price", "quantity", "status")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "name",
        "email",
        "total_amount",
        "is_paid",
        "created_at"
    )

    search_fields = ("email", "name")

    list_filter = ("is_paid", "created_at")

    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "order",
        "product",
        "service",
        "quantity",
        "price",
        "status"
    )