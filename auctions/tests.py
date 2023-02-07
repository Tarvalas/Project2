from django.test import TestCase
from django.contrib.auth import authenticate
from .models import User

# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="test", password="12345")

    def test_correct_user(self):
        user = authenticate(username="test", password="12345")
        self.assertTrue(user is not None and user.is_authenticated)
    
    def test_incorrect_username(self):
        user = authenticate(username="fail", password="12345")
        self.assertFalse(user is not None and user.is_authenticated)
        
    def test_incorrect_password(self):
        user = authenticate(username="test", password="fail")
        self.assertFalse(user is not None and user.is_authenticated)