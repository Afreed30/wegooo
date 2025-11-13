from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_number', 'email', 'created_at']
    search_fields = ['name', 'email']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ['name', 'bus_number', 'operator', 'category', 'total_seats', 'created_at']
    list_filter = ['operator', 'category']
    search_fields = ['name', 'bus_number', 'travels_name']

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ['origin', 'destination', 'distance_km', 'duration_minutes']
    search_fields = ['origin', 'destination']

class SeatInline(admin.TabularInline):
    model = Seat
    extra = 0

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['bus', 'route', 'travel_date', 'departure_time', 'arrival_time', 'fare_amount']
    list_filter = ['travel_date', 'bus', 'route']
    search_fields = ['bus__name', 'route__origin', 'route__destination']
    inlines = [SeatInline]
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Auto-create seats if they don't exist
        if not obj.seats.exists():
            for i in range(1, obj.bus.total_seats + 1):
                Seat.objects.create(
                    schedule=obj,
                    seat_number=str(i),
                    is_available=True
                )

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['seat_number', 'schedule', 'seat_type', 'is_available']
    list_filter = ['is_available', 'schedule']
    search_fields = ['seat_number']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'schedule', 'get_seats', 'status', 'price', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']

    @admin.display(description="Seats")
    def get_seats(self, obj):
        return ", ".join(seat.seat_number for seat in obj.schedule.seats.all())

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'booking', 'amount', 'provider', 'status', 'payment_time']
    list_filter = ['status', 'provider', 'payment_time']
    readonly_fields = ['payment_time']