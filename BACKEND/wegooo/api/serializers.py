from rest_framework import serializers
from .models import User, BusDetails, Booking, RouteInfo

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'created_at', 'updated_at']


class BusDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusDetails
        fields = ['id', 'bus_number', 'route', 'capacity', 'created_at', 'updated_at']


class RouteInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteInfo
        fields = ['id', 'route_name', 'start_location', 'end_location', 'distance_km']


class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    bus = BusDetailsSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'user', 'bus', 'seat_number', 'booking_date']
