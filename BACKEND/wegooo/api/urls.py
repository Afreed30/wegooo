from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user),
    path('login/', views.login_user),
    path('buses/', views.list_buses),
    path('buses/add/', views.add_bus),
    path('routes/', views.list_routes),
    path('routes/add/', views.add_route),
    path('schedules/', views.list_schedules),
    path('schedules/add/', views.add_schedule),
    path('seats/<int:schedule_id>/', views.get_seats_by_schedule),
    path('book/', views.book_ticket),
    path('bookings/<int:user_id>/', views.user_bookings),
    path('cancel/<int:booking_id>/', views.cancel_booking),
]
