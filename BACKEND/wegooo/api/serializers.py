from rest_framework import serializers
from .models import user, bus, route, schedule, seat, booking
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = '__all__'
class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = bus
        fields = '__all__'
class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = route
        fields = '__all__'
class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = schedule
        fields = '__all__' 
        
class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = seat
        fields = '__all__' 