from django.contrib.auth.models import AbstractUser
from django.db import models

class UserRole(models.TextChoices):
    CUSTOMER = 'CUSTOMER', 'Customer'
    ADMIN = 'ADMIN', 'Admin'
    THEATRE_MANAGER = 'THEATRE_MANAGER', 'Theatre Manager'

class User(AbstractUser):
    username = None
    name = models.CharField(max_length = 255, blank = True)
    email = models.EmailField(unique = True)
    phone = models.CharField(max_length = 10, unique = True, null = True, blank = True)
    role = models.CharField(max_length = 20, 
                            choices = UserRole.choices, 
                            default = UserRole.CUSTOMER)
    email_verified = models.BooleanField(default = False)
    updated_at = models.DateTimeField(auto_now = True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f'{self.email} ({self.role})'