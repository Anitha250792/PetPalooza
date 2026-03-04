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
from django.core.mail import send_mail
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings
from .models import ContactMessage
from accounts.models import Review
from core.models import ConsultationBooking
from petpalooza.utils.email_service import send_consultation_confirmation
from petpalooza.utils.email_service import send_welcome_email

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

# Send welcome email
                send_welcome_email(user)

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

def consult_view(request):

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        pet_type = request.POST.get("pet_type")
        message = request.POST.get("message")

        from core.models import ConsultationBooking
        ConsultationBooking.objects.create(
            name=name,
            email=email,
            phone=phone,
            pet_type=pet_type,
            message=message
        )

        from petpalooza.utils.email_service import send_consultation_confirmation
        send_consultation_confirmation(email, name)

        messages.success(request, "Consultation booked successfully!")

    return render(request, "consult.html")

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



def consultnow(request):
    service = Service.objects.first()

    if request.method == "POST":
        name = request.POST.get("name")
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        Review.objects.create(
            name=name,
            rating=rating,
            comment=comment
        )

    reviews = Review.objects.order_by("-created_at")

    return render(request, "consultnow.html", {
        "service": service,
        "reviews": reviews
    })

def contact_view(request):
    form = ContactForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save()
            messages.success(request, f"Your ticket {message.ticket_id} has been created!")
            return redirect('accounts:contact')

    user_messages = ContactMessage.objects.all().order_by("-created_at")

    return render(request, 'contact.html', {
        'form': form,
        'user_messages': user_messages
    })