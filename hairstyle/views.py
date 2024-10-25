# salon/views.py
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import AdminUser, UserProfile
from .models import *
from .serializers import *
from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class AdminRegistrationView(generics.CreateAPIView):
    queryset = AdminUser.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserRegistrationView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



# salon/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import AdminUser, UserProfile
from .serializers import AdminUserSerializer, UserProfileSerializer
from rest_framework.permissions import AllowAny

class AdminLoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        admin_user = authenticate(request, email=email, password=password)
        if admin_user is not None:
            refresh = RefreshToken.for_user(admin_user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'email': admin_user.email,
                'first_name': admin_user.first_name,
                'last_name': admin_user.last_name
            }, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile_number = serializer.validated_data['mobile_number']
        password = serializer.validated_data['password']

        user_profile = UserProfile.objects.filter(phone_number=mobile_number).first()
        
        if user_profile:
            user = authenticate(username=user_profile.user.username, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "message": "Login successful",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid mobile number or password"}, status=status.HTTP_401_UNAUTHORIZED)

class ServiceViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    #permission_classes = [permissions.IsAdminUser]  # Restrict access to admin users
    

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.AllowAny]
    #permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter bookings by the authenticated user
        return self.queryset.filter(user_profile=self.request.user.userprofile)

    def perform_create(self, serializer):
        slot_id = self.request.data.get('slot')
        try:
            slot = AvailableSlot.objects.get(id=slot_id)
            serializer.save(user_profile=self.request.user.userprofile, slot=slot)
        except AvailableSlot.DoesNotExist:
            raise ValidationError("The selected slot is not available.")

    # Optionally, you can add a custom action if you want a specific endpoint
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def history(self, request):
        # Get all bookings for the user
        bookings = self.get_queryset()
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)


class AvailableSlotViewSet(viewsets.ModelViewSet):
    queryset = AvailableSlot.objects.all()
    serializer_class = AvailableSlotSerializer
    permission_classes = [permissions.AllowAny]  # Allow anyone to view available slots

    # Optional: Override to filter slots by service and date
    def get_queryset(self):
        queryset = super().get_queryset()
        service_id = self.request.query_params.get('service', None)
        date = self.request.query_params.get('date', None)

        if service_id is not None:
            queryset = queryset.filter(service_id=service_id)
        if date is not None:
            queryset = queryset.filter(date=date)

        return queryset
    

class CheckoutViewSet(viewsets.ModelViewSet):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        booking_id = self.request.data.get('booking')
        try:
            booking = Booking.objects.get(id=booking_id)
            total_amount = booking.service.total_cost()  # Calculate total amount
            serializer.save(booking=booking, total_amount=total_amount)
        except Booking.DoesNotExist:
            raise serializers.ValidationError("Booking does not exist.")

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def confirm_payment(self, request, pk=None):
        try:
            checkout = self.get_object()
            checkout.payment_status = 'Confirmed'  # Update the payment status
            checkout.payment_date = timezone.now()  # Set the payment date
            checkout.save()
            return Response(CheckoutSerializer(checkout).data, status=status.HTTP_200_OK)
        except Checkout.DoesNotExist:
            return Response({"error": "Checkout not found."}, status=status.HTTP_404_NOT_FOUND)
