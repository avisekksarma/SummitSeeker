from django.db import models
from django.contrib.auth import models as auth_models


class User(auth_models.AbstractUser):
    userType = [
        ('TR', 'Trekker'),
        ('GD', 'Guide'),
    ]
    type = models.CharField(max_length=2, choices=userType,
                            default='TR', blank=False)
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'type','password']

# Create your models here.
