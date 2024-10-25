# salon/serializers.py
from rest_framework import serializers
from .models import AdminUser, UserProfile, Service, AvailableSlot, Booking, Checkout, UserHistory
from django.contrib.auth.models import User

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = ['id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # Password should be write-only

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user
    
class UserLoginSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        mobile_number = attrs.get('mobile_number')
        password = attrs.get('password')

        if not mobile_number:
            raise serializers.ValidationError("Mobile number is required.")
        if not password:
            raise serializers.ValidationError("Password is required.")

        return attrs

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['user', 'phone_number']  # Add other necessary fields

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        profile = UserProfile.objects.create(user=user, **validated_data)
        return profile
    
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'  # Include all fields

class AvailableSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableSlot
        fields = '__all__'  # Include all fields

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user_profile', 'service', 'slot', 'created_at', 'status']
        read_only_fields = ['user_profile', 'created_at', 'status']  # Set read-only fields

    def create(self, validated_data):
        user_profile_data = validated_data.pop('user_profile')
        user_profile, created = UserProfile.objects.get_or_create(**user_profile_data)
        booking = Booking.objects.create(user_profile=user_profile, **validated_data)
        return booking

class CheckoutSerializer(serializers.ModelSerializer):
    booking = BookingSerializer(read_only=True)  # Nested serializer

    class Meta:
        model = Checkout
        fields = '__all__'  # Include all fields

class UserHistorySerializer(serializers.ModelSerializer):
    booking = BookingSerializer(read_only=True)  # Nested serializer

    class Meta:
        model = UserHistory
        fields = '__all__'  # Include all fields

        
