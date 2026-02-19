from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as account_views

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('dog/', views.dog, name='dog'),
    path('cat/', views.cat, name='cat'),
    path('smallpets/', views.smallpets, name='smallpets'),
    path('services/', views.services, name='services'),
    path('brands/', views.brands, name='brands'),
    path('cart/', include('cart.urls')),
    path('about/', views.about, name='about'),
    path('contact/', account_views.contact_view, name='contact'),
    

]

# ✅ MEDIA FILES (important for product images)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
