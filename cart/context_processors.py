from .models import Cart, CartItem

def cart_count(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        count = CartItem.objects.filter(cart=cart).count()
    else:
        count = 0

    return {
        'cart_count': count
    }
