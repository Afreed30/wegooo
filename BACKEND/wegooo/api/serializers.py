from rest_framework import serializers
from .models import bus_details, booking, route_info, user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = '__all__'

class BusDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = bus_details
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    bus = serializers.StringRelatedField()
    class Meta:
        model = booking
        fields = '__all__'

class routeinfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = route_info
        fields = '__all__'
