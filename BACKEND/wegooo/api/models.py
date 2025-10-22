from django.db import models
from io import BytesIO
from django.core.files import File
import qrcode
from django.contrib.auth.models import User
# Create your models here.

class user(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.username

class bus_details(models.Model):
    bus_number = models.CharField(max_length=20, unique=True)
    route = models.CharField(max_length=255)
    capacity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.bus_number

class route_info(models.Model):
    route_name = models.CharField(max_length=255, unique=True)
    start_location = models.CharField(max_length=255)
    end_location = models.CharField(max_length=255)
    distance_km = models.FloatField()
    def __str__(self):
        return self.route_name

class booking(models.Model):
    STATUS_CHOICES = [('pending','Pending'),('confirmed','Confirmed'),('cancelled','Cancelled')]
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    bus = models.ForeignKey(bus_details, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    def __str__(self):
        return f"Booking {self.id} by {self.user.username} on {self.bus.bus_number}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            qr_data = f"Booking ID: {self.id}, User: {self.user.username}, Bus: {self.bus.bus_number}, Seat: {self.seat_number}"
            qr_img = qrcode.make(qr_data)
            buffer = BytesIO()
            qr_img.save(buffer, 'PNG')
            self.qr_code.save(f'booking_{self.id}.png', File(buffer), save=False)
            buffer.close()
            super().save(update_fields=['qr_code'])
        except Exception:
            pass
