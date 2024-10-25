# salon/models.py
from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission

# Custom Manager for AdminUser
class AdminUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

# Custom AdminUser model
class AdminUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = AdminUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(
        Group,
        related_name='adminuser_set',  # Avoid clash
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='adminuser_set',  # Avoid clash
        blank=True,
    )

    def __str__(self):
        return self.email



# Model for User Profile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)



# Model for Services offered by the salon
class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    duration = models.IntegerField(help_text="Duration in minutes")
    image = models.ImageField(upload_to='services/', blank=True, null=True)

    def __str__(self):
        return self.name

    def total_cost(self):
        """Calculate total cost including tax."""
        return self.price + self.tax


# Model for Available Time Slots for each service
class AvailableSlot(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time_slot = models.TimeField()

    class Meta:
        unique_together = ('service', 'date', 'time_slot')

    def __str__(self):
        return f"{self.service.name} on {self.date} at {self.time_slot}"


# Model for Bookings made for services
class Booking(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    slot = models.ForeignKey(AvailableSlot, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"Booking for {self.service.name} by {self.user_profile.phone_number} on {self.slot.date} at {self.slot.time_slot}"


# Model for Checkout information related to bookings
class Checkout(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, default='Pending')
    payment_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Checkout for {self.booking}"


# Model to track actions related to bookings
class UserHistory(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} for {self.booking} on {self.timestamp}"
