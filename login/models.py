from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = [
        ('staff', 'Staff'),
        ('support', 'Support Staff'),
        ('admin', 'Admin'),
    ]


    username = models.CharField(
        max_length=7,

        unique=True,

        validators=[
            RegexValidator(
                r'^\d{6,7}$',
                'Username must contain 6 or 7 digits.'
            )
        ],
    )


    email = models.EmailField(
        blank=True
    )


    full_name = models.CharField(
        max_length=150,
        blank=True
    )


    phone = models.CharField(
        max_length=20,
        blank=True
    )


    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='staff'
    )


    email_verified = models.BooleanField(
        default=False
    )


    def __str__(self):

        return self.username
