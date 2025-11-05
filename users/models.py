from django.contrib.auth.models import AbstractUser
from django.db import models
from league.models import Team

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('fan', 'Fan'),
        ('coach', 'Coach'),
        ('official', 'Official'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='fan')
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)