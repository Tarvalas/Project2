from django.test import TestCase
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import User, Listing, Bid, Comment

# Create your tests here.
class UserModelTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username="test", password="12345")

    def test_correct_user(self):
        user = authenticate(username="test", password="12345")
        self.assertTrue(user is not None and user.is_authenticated)
    
    def test_incorrect_username(self):
        user = authenticate(username="fail", password="12345")
        self.assertFalse(user is not None and user.is_authenticated)
        
    def test_incorrect_password(self):
        user = authenticate(username="test", password="fail")
        self.assertFalse(user is not None and user.is_authenticated)


class ListModelTestCase(TestCase):
    def setUp(self):
        listing = Listing.objects.create(title="Testing", description="description", start_bid=10.00)
        listing.save()

    def test_correct_listing(self):
        listing = Listing.objects.get()
        self.assertTrue(listing is not None)

    def test_incorrect_listing_title(self):
        listing = Listing.objects.create(title="", description="description", start_bid=10.00)
        self.assertRaises(ValidationError, listing.full_clean)

    def test_incorrect_listing_bid_negative(self):
        listing = Listing.objects.create(title="Testing", description="description", start_bid=-10.00)
        self.assertRaises(ValidationError, listing.full_clean)

    def test_incorrect_listing_bid_digits(self):
        listing = Listing.objects.create(title="Testing", description="description", start_bid=10.001)
        self.assertRaises(ValidationError, listing.full_clean)