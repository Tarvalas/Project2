from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from taggit.managers import TaggableManager


class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.username}"


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=80, blank=False)
    description = models.TextField(max_length=800)
    start_bid = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)])
    image_url = models.URLField(blank=True, null=True)
    tags = TaggableManager(blank=True)
    list_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"
    

class Bid(models.Model):
    pass


class Comment(models.Model):
    pass