from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    Custom user manager where email is the unique identifier for authentication
    instead of usernames.
    """
    def create_user(self, email, phone_number, password=None, **extra_fields):
        """
        Create and return a regular user with an email, phone number, and password.
        """
        if not email:
            raise ValueError(_('The Email field must be set'))
        if not phone_number:
            raise ValueError(_('The Phone Number field must be set'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        """
        Create and return a superuser with admin rights.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, phone_number, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model where email is the unique identifier instead of usernames.
    """
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('username'), max_length=30, unique=True, blank=True, null=True)
    phone_number = models.CharField(_('phone number'), max_length=15, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True, null=True)
    date_of_birth = models.DateField(_('date of birth'), blank=True, null=True)
    address = models.TextField(_('address'), blank=True, null=True)
    bio = models.TextField(_('bio'), blank=True, null=True)
    profile_picture = models.ImageField(_('profile picture'), upload_to='profile_pics/', blank=True, null=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return self.email
