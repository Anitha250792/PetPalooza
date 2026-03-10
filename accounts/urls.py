from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("login/", views.login_view, name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('account/', views.account_dashboard, name='account'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('search/', views.search, name='search'),
    path('petservice/', views.petservice_view, name='petservice'),
    path('contact/', views.contact_view, name='contact'),
    path('consult/', views.consult_view, name='consult'),
    path('consultnow/', views.consultnow, name='consultnow'),
    
]
