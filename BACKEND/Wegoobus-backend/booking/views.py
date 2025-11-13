from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes, action,api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.conf import settings
import razorpay
from datetime import datetime
from .models import *
from .serializers import *
from io import BytesIO
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode import qr
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from io import BytesIO
import qrcode
from .models import Booking

# Create your views here.
# Authentication Views
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Check if user exists
    user_obj = User.objects.filter(username=username).first()
    if not user_obj:
        return Response({'error': 'User does not exist'}, status=404)

    # Authenticate user
    user = authenticate(username=username, password=password)

    if not user:
        return Response({'error': 'Invalid credentials'}, status=401)

    # Login OK
    token, created = Token.objects.get_or_create(user=user)
    return Response({
        'token': token.key,
        'user': UserSerializer(user).data
    })

@api_view(['POST'])
def logout(request):
    request.user.auth_token.delete()
    return Response({'message': 'Logged out successfully'})

# Bus Search View
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def search_buses(request):
    origin = request.query_params.get('origin', '').strip().lower()
    destination = request.query_params.get('destination', '').strip().lower()
    travel_date = request.query_params.get('travel_date', '').strip()

    if not origin or not destination or not travel_date:
        return Response(
            {'error': 'Origin, destination, and travel date are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Filter routes ignoring case & spaces
    routes = Route.objects.filter(
        origin__iexact=origin,
        destination__iexact=destination
    )

    schedules = Schedule.objects.filter(
        route__in=routes,
        travel_date=travel_date
    ).select_related('bus', 'route')

    # ✅ VERY IMPORTANT: Return list always
    serializer = ScheduleSerializer(schedules, many=True)
    return Response(serializer.data)

# Schedule ViewSet
class ScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['get'])
    def seats(self, request, pk=None):
        schedule = self.get_object()
        seats = schedule.seats.all()
        serializer = SeatSerializer(seats, many=True)
        return Response(serializer.data)

# Booking ViewSet
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)

    def create(self, request):
        seat_id = request.data.get('seat')
        schedule_id = request.data.get('schedule')

        # ✅ Get passenger details from request
        passenger_name = request.data.get('passenger_name')
        passenger_age = request.data.get('passenger_age')
        passenger_gender = request.data.get('passenger_gender')

        try:
            seat = Seat.objects.get(id=seat_id)
            schedule = Schedule.objects.get(id=schedule_id)

            if not seat.is_available:
                return Response({'error': 'Seat is not available'},
                                status=status.HTTP_400_BAD_REQUEST)

            # ✅ Create booking with passenger details saved
            booking = Booking.objects.create(
                user=request.user,
                schedule=schedule,
                seat=seat,
                price=schedule.fare_amount,
                status='CONFIRMED',  # set directly to confirmed or keep PENDING
                passenger_name=passenger_name,
                passenger_age=passenger_age,
                passenger_gender=passenger_gender,
            )

            # ✅ Update seat status
            seat.is_available = False
            seat.save()

            serializer = BookingSerializer(booking)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except (Seat.DoesNotExist, Schedule.DoesNotExist):
            return Response({'error': 'Invalid seat or schedule'},
                            status=status.HTTP_400_BAD_REQUEST)

# Payment Views
@api_view(['POST'])
def create_payment_order(request):
    booking_id = request.data.get('booking_id')

    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        amount = int(float(booking.price) * 100)

        order = client.order.create({
            'amount': amount,
            'currency': 'INR',
            'receipt': f'booking_{booking.id}',
            'payment_capture': 1
        })

        return Response({
            'order_id': order['id'],
            'amount': amount,
            'currency': 'INR',
            'key': settings.RAZORPAY_KEY_ID
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['POST'])
def verify_payment(request):
    payment_id = request.data.get('razorpay_payment_id')
    order_id = request.data.get('razorpay_order_id')
    signature = request.data.get('razorpay_signature')
    booking_id = request.data.get('booking_id')
    
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
        
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        # Verify signature
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        
        client.utility.verify_payment_signature(params_dict)
        
        # Create payment record
        payment = Payment.objects.create(
            booking=booking,
            amount=booking.price,
            provider='Razorpay',
            status='SUCCESS'
        )
        
        # Update booking status
        booking.status = 'CONFIRMED'
        booking.save()
        
        return Response({
            'message': 'Payment successful',
            'payment_id': payment.id
        })
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Admin Views (for managing buses, routes, schedules)
class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

class ScheduleAdminViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAdminUser]

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ticket_pdf(request, pk):

    booking = get_object_or_404(
        Booking.objects.select_related("schedule__bus", "schedule__route", "seat"),
        id=pk,
        user=request.user
    )

    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    W, H = A4

    # --- Background ---
    c.setFillColor(HexColor("#10071f"))
    c.rect(0, 0, W, H, stroke=0, fill=1)

    # --- Ticket Card ---
    card_x, card_y = 50, 140
    card_w, card_h = W - 100, H - 240

    c.setFillColor(HexColor("#ffffff"))
    c.roundRect(card_x, card_y, card_w, card_h, 24, stroke=0, fill=1)

    # --- Top Header Bar ---
    c.setFillColor(HexColor("#7F27FF"))
    header_h = 90
    c.roundRect(card_x, card_y + card_h - header_h, card_w, header_h, 24, stroke=0, fill=1)

    # Logo (Optional)
    try:
        logo = ImageReader("static/bus.png")
        c.drawImage(logo, card_x + 30, card_y + card_h - 70, width=75, height=45, mask='auto')
    except:
        pass

    # Title
    c.setFillColor("#FFFFFF")
    c.setFont("Helvetica-Bold", 24)
    c.drawString(card_x + 120, card_y + card_h - 55, "WEGOOO BUS TICKET")

    # --- Passenger & Trip Details ---
    c.setFillColor("#000000")
    c.setFont("Helvetica", 14)
    y = card_y + card_h - 130
    gap = 28

    def write(label, val):
        nonlocal y
        c.setFont("Helvetica-Bold", 13)
        c.drawString(card_x + 50, y, f"{label}:")
        c.setFont("Helvetica", 13)
        c.drawString(card_x + 190, y, str(val))
        y -= gap

    write("Passenger", booking.passenger_name or "-")
    write("Bus", booking.schedule.bus.name)
    write("Route", f"{booking.schedule.route.origin} → {booking.schedule.route.destination}")
    write("Travel Date", booking.schedule.travel_date)
    write("Departure", booking.schedule.departure_time)
    write("Arrival", booking.schedule.arrival_time)
    write("Seat", booking.seat.seat_number)
    write("Amount", f"₹{booking.price}")
    # --- Boarding Barcode Strip ---
    barcode_text = f"{booking.id}-{booking.seat.seat_number}-{booking.schedule.travel_date}"
    barcode = qrcode.make(barcode_text)  # Using QR as scannable barcode style

    barcode_buf = BytesIO()
    barcode.save(barcode_buf, format="PNG")
    barcode_buf.seek(0)
    barcode_img = ImageReader(barcode_buf)

    # Draw long barcode style on bottom
    c.drawImage(barcode_img, 50, 20, width=W - 100, height=40)


    # --- Price Highlight ---
    c.setFont("Helvetica-Bold", 26)
    c.setFillColor(HexColor("#7F27FF"))
    c.drawString(card_x + 50, card_y + 60, f"₹{booking.price}")


    # --- Tear Line Separator (Dotted) ---
    c.setDash(1, 3)  # 1px line, 3px gap
    c.setStrokeColor(HexColor("#C7C4D4"))
    c.setLineWidth(1)
    c.line(card_x + 40, y, card_x + card_w - 40, y)

    c.setDash()  # reset dash

    # Move down below the line
    y -= 40

    # --- Price & QR Section ---
    c.setFont("Helvetica-Bold", 26)
    c.setFillColor(HexColor("#7F27FF"))
    c.drawString(card_x + 50, y, f"₹{booking.price}")

    # QR Code (unchanged)
    qr_content = f"Wegooo Ticket #{booking.id} | Seat {booking.seat.seat_number}"
    qr = qrcode.make(qr_content)
    qr_io = BytesIO()
    qr.save(qr_io, format="PNG")
    qr_io.seek(0)
    qr_img = ImageReader(qr_io)
    c.drawImage(qr_img, card_x + card_w - 150, card_y + 35, width=100, height=100)


    c.save()
    pdf = buf.getvalue()
    buf.close()

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename=Wegooo_Ticket_{booking.id}.pdf"'
    return response
