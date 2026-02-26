
from cart.models import Product
from django.shortcuts import render
from django.db.models import Q

def dog(request):
    products = Product.objects.filter(category="Dog")

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    rating = request.GET.get('rating')
    sort = request.GET.get('sort')

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    if rating:
        products = products.filter(rating__gte=rating)

    if sort == "low":
        products = products.order_by('price')
    elif sort == "high":
        products = products.order_by('-price')
    elif sort == "rating":
        products = products.order_by('-rating')

    return render(request, "dog.html", {"products": products})

def addtocart(request):
    return render(request, 'addtocart.html')

def cat(request):
    products = Product.objects.filter(category__iexact="cat")

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    rating = request.GET.get('rating')
    sort = request.GET.get('sort')

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    if rating:
        products = products.filter(rating__gte=rating)

    if sort == "low":
        products = products.order_by('price')
    elif sort == "high":
        products = products.order_by('-price')
    elif sort == "rating":
        products = products.order_by('-rating')

    return render(request, "cat.html", {"products": products})


def smallpets(request):
    products = Product.objects.filter(category__iexact="smallpets")

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    rating = request.GET.get('rating')
    sort = request.GET.get('sort')

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    if rating:
        products = products.filter(rating__gte=rating)

    if sort == "low":
        products = products.order_by('price')
    elif sort == "high":
        products = products.order_by('-price')
    elif sort == "rating":
        products = products.order_by('-rating')

    return render(request, "smallpets.html", {"products": products})





# views.py
def about(request):
    return render(request, 'about.html')



