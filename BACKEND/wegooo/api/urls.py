from django.urls import path
from . import views

urlpatterns = [
    path('buses/', views.list_buses),
    path('booking/', views.create_booking),
    path('payment/', views.create_payment),
]
