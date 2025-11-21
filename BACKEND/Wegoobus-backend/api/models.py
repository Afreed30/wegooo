from django.db import models

from django.contrib.auth.models import User  # using Django default user
# Create your models here.
class Operator(models.Model):
    name = models.CharField(max_length=128)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Bus(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE, related_name="buses")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="buses")

    name = models.CharField(max_length=128)
    travels_name = models.CharField(max_length=128, blank=True, null=True)
    bus_number = models.CharField(max_length=20, blank=True, null=True)
    total_seats = models.IntegerField()
    amenities = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.bus_number})"


class Route(models.Model):
    origin = models.CharField(max_length=128)
    destination = models.CharField(max_length=128)
    distance_km = models.IntegerField(blank=True, null=True)
    duration_minutes = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.origin} → {self.destination}"


class Schedule(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name="schedules")
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="schedules")
    travel_date = models.DateField()
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    fare_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bus.name} on {self.travel_date}"


class Seat(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="seats")
    seat_number = models.CharField(max_length=10)
    seat_type = models.CharField(max_length=32, blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.seat_number} - {self.schedule.bus.name}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="bookings")
    seat = models.ForeignKey(Seat, on_delete=models.SET_NULL, null=True, blank=True, related_name="bookings")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    passenger_name = models.CharField(max_length=100, blank=True, null=True)
    passenger_age = models.PositiveIntegerField(blank=True, null=True)
    passenger_gender = models.CharField(
        max_length=1,
        choices=[("M", "Male"), ("F", "Female")],
        blank=True,
        null=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)
    cancellation_reason = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"Booking #{self.id} - {self.user.username} - {self.status} - {self.seat.seat_number if self.seat else 'No Seat'}"

class Payment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    ]
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    provider = models.CharField(max_length=64, blank=True, null=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='PENDING')
    payment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment #{self.id} - {self.status}"

