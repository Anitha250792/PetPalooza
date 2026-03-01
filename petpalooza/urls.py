from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # accounts app
    path('', include('accounts.urls')),

    # cart app
    path('cart/', include('cart.urls')),
]