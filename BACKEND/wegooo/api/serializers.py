from rest_framework import serializers
from django.contrib.auth.models import User
from .models import user, bus, route, schedule, seat, booking
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

# Serializer for your custom `user` model (if you still use it elsewhere)
class AppUserSerializer(serializers.ModelSerializer):
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

# -- Registration serializer using Django's built-in User (recommended) --
class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm password")

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_instance = User.objects.create_user(username=username, email=email, password=password)
        return user_instance
