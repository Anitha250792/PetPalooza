from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path("", views.home_view, name="home"),
    path("login/", views.login_view, name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('search/', views.search, name='search'),
    path('petservice/', views.petservice_view, name='petservice'),
    path('contact/', views.contact_view, name='contact'),
    path('consult/', views.consult_view, name='consult'),
]
