from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from taggit.managers import TaggableManager


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', related_name='watchlist', blank=True)
    num_watchlist = models.IntegerField(default=0, blank=True)

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
    num_bids = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title}"
    

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid_time = models.DateTimeField(auto_now_add=True)
    bid = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)])

    def __str__(self):
        return f"${self.bid} by {self.user}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField(max_length=3000)
    comment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"comment by {self.user} about {self.item}"