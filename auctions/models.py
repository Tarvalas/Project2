from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=80, blank=False)
    description = models.TextField(max_length=800)
    start_bid = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)])

class Bid(models.Model):
    pass

class Comment(models.Model):
    pass