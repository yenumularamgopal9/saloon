# salon/urls.py
from django.urls import path, include
from .views import AdminRegistrationView, UserRegistrationView, AdminLoginView,UserLoginView
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()
router.register(r'services', ServiceViewSet)
router.register(r'bookings', BookingViewSet)  # Add the BookingViewSet
router.register(r'available-slots', AvailableSlotViewSet)  # Add AvailableSlotViewSet
router.register(r'checkouts', CheckoutViewSet)  # Add CheckoutViewSet




urlpatterns = [
    path('register/admin/', AdminRegistrationView.as_view(), name='admin-register'),
    path('register/user/', UserRegistrationView.as_view(), name='user-register'),
     path('login/admin/', AdminLoginView.as_view(), name='admin-login'),
    path('login/user/', UserLoginView.as_view(), name='user-login'),
    path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


]
