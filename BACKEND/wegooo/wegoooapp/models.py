from django.db import models

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
class booking(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    bus = models.ForeignKey(bus_details, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Booking {self.id} by {self.user.username} on bus {self.bus.bus_number}"
class route_info(models.Model):
    route_name = models.CharField(max_length=255, unique=True)
    start_location = models.CharField(max_length=255)
    end_location = models.CharField(max_length=255)
    distance_km = models.FloatField()
    def __str__(self):
        return self.route_name