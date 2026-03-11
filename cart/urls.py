from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_page, name='cart_page'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
     path('increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('remove/<int:item_id>/', views.remove_item, name='remove_item'),
    path('checkout/', views.checkout_view, name='checkout'),
    path("payment-success/", views.payment_success, name="payment_success"),
    path("thankyou/<int:order_id>/", views.thankyou, name="thankyou"),
    path("track-order/<int:order_id>/", views.track_order, name="track_order"),
    path('add-service/<int:service_id>/', views.add_service_to_cart, name='add_service_to_cart'),
    path('remove-service/<str:service_id>/', views.remove_service_item, name='remove_service_item'),
    
]

