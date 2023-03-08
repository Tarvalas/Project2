from django.test import TestCase
from django.contrib.auth import authenticate, get_user
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from http import HTTPStatus
from django.core.exceptions import ValidationError
from .models import User, Listing, Bid, Comment
from .forms import RegisterForm, LoginForm, ListingForm

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


class CreateListingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="12345")
        user_data = {
            'username': 'test',
            'password': '12345'
        }
        response = self.client.post(reverse('login'), user_data)
        self.assertRedirects(response, reverse('index'))
    
    def test_user_is_loggedin(self):
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)
    
    def test_listing_create_page(self):
        response = self.client.get(reverse('create_listing'))
        self.assertTemplateUsed(response, 'auctions/listing_create.html')
    
    def test_listing_create_page_form(self):
        response = self.client.get(reverse('create_listing'))
        form = response.context.get('form')
        self.assertIsInstance(form, ListingForm)

    def test_listing_form(self):
        form = ListingForm({
            'title': 'Test',
            'description': 'Test Description',
            'start_bid': 10.00,
            'image_url': 'http://www.google.com', # Not required
            'category': 'test_category' # Not required
        })
        form.instance.user = get_user(self.client)
        self.assertTrue(form.is_valid())
        listing = form.save()
        self.assertEqual(listing.title, 'Test')
        self.assertEqual(listing.description, 'Test Description')
        self.assertEqual(listing.start_bid, 10.00)
        self.assertEqual(listing.image_url, 'http://www.google.com')
        self.assertEqual(listing.category, 'test_category')


