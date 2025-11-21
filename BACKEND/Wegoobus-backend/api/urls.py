from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import ticket_pdf

router = DefaultRouter()
router.register(r'schedules', views.ScheduleViewSet, basename='schedule')
router.register(r'bookings', views.BookingViewSet, basename='booking')
router.register(r'buses', views.BusViewSet, basename='bus')
router.register(r'routes', views.RouteViewSet, basename='route')
router.register(r'admin/schedules', views.ScheduleAdminViewSet, basename='admin-schedule')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('search-buses/', views.search_buses, name='search-buses'),
    path('create-payment-order/', views.create_payment_order, name='create-payment-order'),
    path('verify-payment/', views.verify_payment, name='verify-payment'),
    path("bookings/<int:pk>/ticket/pdf/", ticket_pdf, name="booking-ticket-pdf"),

]