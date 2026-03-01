from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from .forms import ContactForm
from core.models import HeroSlide, PetCategory, PromoSection, ServiceCard
from cart.models import Product
from django.db.models import Q
from django.db import connection
from cart.models import Service

def login_view(request):

    if request.method == "POST":

        # LOGIN PROCESS
        if "login_btn" in request.POST:
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("/")  # redirect to home
            else:
                messages.error(request, "Invalid email or password")

        # REGISTER PROCESS
        if "register_btn" in request.POST:
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            password = request.POST.get("password")

            if User.objects.filter(username=email).exists():
                messages.error(request, "Email already exists")
            else:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                messages.success(request, "Account created successfully!")
                return redirect("/")

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("/")

def home_view(request):
    hero_slides = HeroSlide.objects.filter(is_active=True)
    pet_categories = PetCategory.objects.all()
    promo_sections = PromoSection.objects.all()
    service_cards = ServiceCard.objects.all()

    return render(request, "home.html", {
        "hero_slides": hero_slides,
        "pet_categories": pet_categories,
        "promo_sections": promo_sections,
        "service_cards": service_cards,
    })

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

def search(request):
    query = request.GET.get('q')
    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(category__icontains=query)
        )

    return render(request, "search.html", {
        "products": products,
        "query": query
    })


def petservice_view(request):
    return render(request, "petservice.html")



def consult_view(request):
    return render(request, "consult.html")

def consultnow(request):
    service = Service.objects.first()   # or filter specific one
    return render(request, "consultnow.html", {"service": service})