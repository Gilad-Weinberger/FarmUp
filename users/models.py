from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from base.models import *
import random
import string

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('worker', 'Worker'),
        ('farmer', 'Farmer'),
        ('admin', 'Admin'),
    ]

    user_id = models.CharField(unique=True, max_length=20, null=True, blank=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    user_type = models.CharField(max_length=30, choices=USER_TYPE_CHOICES, null=True)

    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(max_length=10)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.CharField(max_length=100, null=True, blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Avoids clash with auth.User.groups
        blank=True,
        help_text=_('The groups this user belongs to.'),
        verbose_name=_('groups'),
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Avoids clash with auth.User.user_permissions
        blank=True,
        help_text=_('Specific permissions for this user.'),
        verbose_name=_('user permissions'),
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name} | {self.user_type}"
    
    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = self.generate_unique_user_id()
        super().save(*args, **kwargs)
    
    def generate_unique_user_id(self):
        characters = string.ascii_uppercase + string.digits
        while True:
            random_id = ''.join(random.choices(characters, k=20))
            if not User.objects.filter(user_id=random_id).exists(): 
                return random_id
    
    