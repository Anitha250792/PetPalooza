
from cart.models import Product
from django.shortcuts import render

def dog(request):
    products = Product.objects.filter(category="Dog")
    return render(request, 'dog.html', {'products': products})

def addtocart(request):
    return render(request, 'addtocart.html')

def cat(request):
    products = Product.objects.filter(category__iexact="cat")
    return render(request, "cat.html", {"products": products})


def smallpets(request):
    products = Product.objects.filter(category__iexact="smallpets")
    return render(request, "smallpets.html", {"products": products})

def services(request):
    return render(request, 'services.html')

def brands(request):
    return render(request, 'brands.html')

# views.py
def about(request):
    return render(request, 'about.html')

