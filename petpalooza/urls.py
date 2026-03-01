from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as account_views

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Accounts app
    path('', include('accounts.urls')),

    # Cart app
    path('cart/', include('cart.urls')),
]

# ✅ MEDIA FILES (important for product images)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
