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
class bus(models.Model):
    bus_type = [
        ('SEATER_NON_AC', 'Seater Non-A/C'),
        ('SLEEPER_NON_AC', 'Sleeper Non-A/C'),
        ('SEATER_AC', 'Seater A/C'),
        ('SLEEPER_AC', 'Sleeper A/C'),
        ('SLEEPER & SEATER_AC','Sleeper/Seater A/C'),
    ]
    bus_number = models.CharField(max_length=20, unique=True)
    bus_name = models.CharField(max_length=100)
    bus_type = models.CharField(max_length=50, choices=bus_type)
    total_seats = models.IntegerField()
    amenities = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.bus_name} ({self.bus_number})"
class route(models.Model):
   from_location = models.CharField(max_length=100)
   to_location = models.CharField(max_length=100)
   distance_km = models.FloatField(help_text="Distance in kilometers")
   duration = models.DurationField(help_text="Estimated travel duration") 
   base_fare = models.DecimalField(max_digits=10,decimal_places=2)
   created_at = models.DateTimeField(auto_now_add=True)
   def __str__(self):
       return f"{self.from_location} to {self.to_location}"
class schedule(models.Model):
    bus = models.ForeignKey(bus, on_delete=models.CASCADE)
    route = models.ForeignKey(route, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    available_seats = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.bus.bus_name} on {self.route} at {self.departure_time}"
class seat(models.Model):
    seat_type = [
        ('WINDOW', 'window'),
        ('AISLE', 'aisle'),
        ('MIDDLE', 'middle'),
        ('UPPER', 'upper'),
        ('LOWER', 'lower'),
    ]
    schedule = models.ForeignKey(schedule, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=5)
    seat_type = models.CharField(max_length=10, choices=seat_type)
    is_booked = models.BooleanField(default=False)
    def __str__(self): 
        return f"Seat {self.seat_number} on {self.schedule}"
class booking(models.Model):
    booking_status = [
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('PENDING', 'Pending'),
    ]
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    schedule = models.ForeignKey(schedule, on_delete=models.CASCADE)
    seat = models.ForeignKey(seat, on_delete=models.CASCADE)
    booking_number = models.CharField(max_length=20, unique=True)
    passenger_name = models.CharField(max_length=100)
    passenger_age = models.IntegerField()
    passenger_gender = models.CharField(max_length=10)
    passenger_number = models.CharField(max_length=15)
    booking_date = models.DateTimeField(auto_now_add=True)
    total_fare = models.DecimalField(max_digits=10, decimal_places=2)
    booking_status = models.CharField(max_length=10, choices=booking_status)
    
    def __str__(self):
        return f"Booking {self.booking_number} for {self.passenger_name}"
    