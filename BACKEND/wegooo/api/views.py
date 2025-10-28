from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
import uuid

from .models import user, bus, route, schedule, seat, booking
from .serializers import (
    UserRegisterSerializer,
    BusSerializer,
    RouteSerializer,
    ScheduleSerializer,
    SeatSerializer,
    BookingSerializer,
)

# ----------------------------- USER AUTH VIEWS -----------------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user_obj = serializer.save()
        token, _ = Token.objects.get_or_create(user=user_obj)
        return Response({
            "message": "User registered successfully",
            "token": token.key,
            "user_id": user_obj.id
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get("email")
    password = request.data.get("password")

    try:
        usr = user.objects.get(email=email, password=password)
        token, _ = Token.objects.get_or_create(user=usr)
        return Response({
            "message": "Login successful",
            "token": token.key,
            "user_id": usr.id
        }, status=status.HTTP_200_OK)
    except user.DoesNotExist:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# ----------------------------- BUS VIEWS -----------------------------
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_buses(request):
    buses = bus.objects.all()
    serializer = BusSerializer(buses, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_bus(request):
    serializer = BusSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Bus added successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------------------- ROUTE VIEWS -----------------------------
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_routes(request):
    routes = route.objects.all()
    serializer = RouteSerializer(routes, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_route(request):
    serializer = RouteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Route added successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------------------- SCHEDULE VIEWS -----------------------------
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_schedules(request):
    schedules = schedule.objects.select_related("bus", "route").all()
    serializer = ScheduleSerializer(schedules, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_schedule(request):
    serializer = ScheduleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Schedule added successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------------------- SEAT VIEWS -----------------------------
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_seats_by_schedule(request, schedule_id):
    seats = seat.objects.filter(schedule_id=schedule_id)
    serializer = SeatSerializer(seats, many=True)
    return Response(serializer.data)


# ----------------------------- BOOKING VIEWS -----------------------------
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def book_ticket(request):
    user_id = request.data.get("user")
    schedule_id = request.data.get("schedule")
    seat_id = request.data.get("seat")

    user_obj = get_object_or_404(user, id=user_id)
    schedule_obj = get_object_or_404(schedule, id=schedule_id)
    seat_obj = get_object_or_404(seat, id=seat_id)

    if seat_obj.is_booked:
        return Response({"error": "Seat already booked"}, status=status.HTTP_400_BAD_REQUEST)

    booking_number = str(uuid.uuid4())[:8].upper()

    data = {
        "user": user_obj.id,
        "schedule": schedule_obj.id,
        "seat": seat_obj.id,
        "booking_number": booking_number,
        "passenger_name": request.data.get("passenger_name"),
        "passenger_age": request.data.get("passenger_age"),
        "passenger_gender": request.data.get("passenger_gender"),
        "passenger_number": request.data.get("passenger_number"),
        "total_fare": request.data.get("total_fare"),
        "booking_status": "CONFIRMED",
    }

    serializer = BookingSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        seat_obj.is_booked = True
        seat_obj.save()
        return Response({
            "message": "Booking successful",
            "booking_number": booking_number
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_bookings(request, user_id):
    # Only allow users to see their own bookings
    if request.user.id != user_id:
        return Response({"error": "You are not authorized to view this user's bookings."},
                        status=status.HTTP_403_FORBIDDEN)
    bookings = booking.objects.filter(user_id=user_id).select_related("schedule", "seat")
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cancel_booking(request, booking_id):
    try:
        book = booking.objects.get(id=booking_id)
        if book.user != request.user:
            return Response({"error": "You are not allowed to cancel this booking."},
                            status=status.HTTP_403_FORBIDDEN)

        book.booking_status = "CANCELLED"
        book.seat.is_booked = False
        book.seat.save()
        book.save()
        return Response({"message": "Booking cancelled successfully"}, status=status.HTTP_200_OK)
    except booking.DoesNotExist:
        return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
