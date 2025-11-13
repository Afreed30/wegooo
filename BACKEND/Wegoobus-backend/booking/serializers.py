# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Operator, Category, Bus, Route, Schedule, Seat, Booking, Payment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BusSerializer(serializers.ModelSerializer):
    operator_name = serializers.CharField(source='operator.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Bus
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    bus_details = BusSerializer(source='bus', read_only=True)
    route_details = RouteSerializer(source='route', read_only=True)
    available_seats = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = '__all__'

    def get_available_seats(self, obj):
        return obj.seats.filter(is_available=True).count()

class BookingSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    schedule_details = ScheduleSerializer(source='schedule', read_only=True)
    seat_details = SeatSerializer(source='seat', read_only=True)
    passenger_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    passenger_age = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    passenger_gender = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ["user"]

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'