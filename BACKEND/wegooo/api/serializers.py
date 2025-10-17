from rest_framework import serializers
from wegoooapp.models import bus_details,Booking,route_info,user
class BusDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = bus_details
        fields = ['bus_number', 'route', 'capacity', 'created_at', 'updated_at']
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['user', 'bus', 'seat_number', 'booking_date']
class routeinfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = route_info
        fields = ['route_name', 'start_location', 'end_location', 'distance_km']
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ['username', 'email', 'password', 'created_at', 'updated_at']