from django.test import TestCase
from django.contrib.auth import authenticate, get_user
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from http import HTTPStatus
from django.core.exceptions import ValidationError
from .models import User, Listing, Bid, Comment
from .forms import RegisterForm, LoginForm

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
        user = User.objects.create_user(username="test", password="12345")
        listing = Listing.objects.create(user=user, title="Testing", description="description", start_bid=10.00)
        listing.save()

    def test_correct_listing(self):
        listing = Listing.objects.get()
        self.assertTrue(listing is not None)

    def test_incorrect_listing_title(self):
        user = User.objects.create_user(username="test2", password="12345")
        listing = Listing.objects.create(user=user, title="", description="description", start_bid=10.00)
        self.assertRaises(ValidationError, listing.full_clean)

    def test_incorrect_listing_bid_negative(self):
        user = User.objects.create_user(username="test2", password="12345")
        listing = Listing.objects.create(user=user, title="Testing", description="description", start_bid=-10.00)
        self.assertRaises(ValidationError, listing.full_clean)

    def test_incorrect_listing_bid_digits(self):
        user = User.objects.create_user(username="test2", password="12345")
        listing = Listing.objects.create(user=user, title="Testing", description="description", start_bid=10.001)
        self.assertRaises(ValidationError, listing.full_clean)
    
    def test_tag_adding(self):
        listing = Listing.objects.first()
        listing.tags.add("watch", "Car", "!!!")
        listing_tags = set(listing.tags.names())
        tag_names = {"watch", "Car", "!!!"}
        self.assertEqual(listing_tags, tag_names)

    def test_tag_delete(self):
        listing = Listing.objects.first()
        listing.tags.add("watch", "Car", "!!!")
        listing.tags.remove("watch")
        listing_tags = set(listing.tags.names())
        tag_names = {"Car", "!!!"}
        self.assertEqual(listing_tags, tag_names)


class UserRegistrationFormTests(TestCase):
    def setUp(self):
        form_data = {
            'username': 'testing_name',
            'email': 'testing_email@example.com',
            'password1': 'confirmation',
            'password2': 'confirmation'
        }
        self.form = RegisterForm(form_data)
        if self.form.is_valid():
            self.form.save()
    
    def test_registration_form_class(self):
         self.assertTrue(issubclass(type(self.form), UserCreationForm))
    
    def test_registration_form_submit_class(self):
        form_db_object = User.objects.first()
        self.assertTrue(issubclass(type(form_db_object), User))

    def test_user_registration(self):
        user = authenticate(username = 'testing_name', password = 'confirmation')
        self.assertTrue(user is not None and user.is_authenticated)


class UserLoginTest(TestCase):
    def setUp(self):
        self.username = 'testing_name'
        self.email = 'testing_email@example.com'
        self.password = 'confirmation'

        form_data = {
            'username': self.username,
            'email': self.email,
            'password1': self.password,
            'password2': self.password
        }
        self.form = RegisterForm(form_data)
        if self.form.is_valid():
            self.form.save()
    
    def test_user_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'auctions/login.html')

    def test_user_login_page_form(self):
        response = self.client.get(reverse('login'))
        form = response.context.get('form')
        self.assertIsInstance(form, LoginForm)

    def test_user_login_works(self):
        user_data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post(reverse('login'), user_data)
        self.assertRedirects(response, reverse('index'))