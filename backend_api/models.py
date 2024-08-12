from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
from django.utils import timezone # type: ignore

class LandlordManager(BaseUserManager):
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

class Landlord(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    nrc_number = models.CharField(max_length=20)
    home_address = models.TextField()
    contact = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='landlord_set',
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        verbose_name=_('groups')
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='landlord_set',
        blank=True,
        help_text=_('Specific permissions for this user.'),
        verbose_name=_('user permissions')
    )

    objects = LandlordManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth', 'nrc_number', 'home_address', 'contact']

    def __str__(self):
        return self.email

class Admin(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    contact = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='admin_set',
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        verbose_name=_('groups')
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='admin_set',
        blank=True,
        help_text=_('Specific permissions for this user.'),
        verbose_name=_('user permissions')
    )

    objects = LandlordManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'contact']

    def __str__(self):
        return self.email

class ListingType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Listing(models.Model):
    STATUS_CHOICES = [
        ('deactivated', 'Deactivated'),
        ('activated', 'Activated'),
        ('occupied', 'Occupied'),
    ]
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE, related_name='listings')
    province = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    number_of_rooms = models.IntegerField()
    details = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    featured = models.BooleanField(default=False)
    address = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    listing_type = models.ForeignKey(ListingType, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='deactivated')

    def __str__(self):
        return f'{self.address} - {self.listing_type.name}'

    def is_old(self):
        return timezone.now() > self.date + timedelta(days=90)

class Gallery(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='galleries')
    image = models.ImageField(upload_to='listing_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.listing.address} - {self.id}'
