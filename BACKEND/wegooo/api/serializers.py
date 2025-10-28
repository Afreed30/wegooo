from rest_framework import serializers
from django.contrib.auth.models import User
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
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = booking
        fields = '__all__'
class UserregisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    def create(self, validated_data):
        user_instance = user(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user_instance.set_password(validated_data['password'])
        user_instance.save()
        return user_instance