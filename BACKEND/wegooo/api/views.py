from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import booking, bus_details, user
from .serializers import BookingSerializer, BusDetailsSerializer
import razorpay

@api_view(['GET'])
def list_buses(request):
    buses = bus_details.objects.all()
    serializer = BusDetailsSerializer(buses, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_booking(request):
    try:
        bus = bus_details.objects.get(id=request.data['bus_id'])
        user_obj = user.objects.get(id=request.data['user_id'])
        seat_number = int(request.data['seat_number'])
        if booking.objects.filter(bus=bus, seat_number=seat_number).exists():
            return Response({'error': 'Seat already booked'}, status=400)
        new_booking = booking.objects.create(user=user_obj, bus=bus, seat_number=seat_number, payment_status='confirmed')
        return Response(BookingSerializer(new_booking).data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['POST'])
def create_payment(request):
    # Razorpay stub - replace keys in production
    try:
        client = razorpay.Client(auth=("YOUR_RAZORPAY_KEY_ID", "YOUR_RAZORPAY_SECRET_KEY"))
        amount = int(request.data.get('amount', 100)) * 100
        payment = client.order.create({'amount': amount, 'currency': 'INR'})
        return Response(payment)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

