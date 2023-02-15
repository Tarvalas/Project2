from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import User, Listing, Bid, Comment


class RegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].label = ''
            self.fields[fieldname].help_text = None

        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control', 'autofocus': True, 'name': 'username', 'placeholder': 'Username'})
        self.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control', 'name': 'email', 'placeholder': 'Email Address'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password', 'placeholder': 'Enter Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'name': 'confirmation', 'placeholder': 'Confirm Password'})

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]


class LoginForm(AuthenticationForm):
    def __init__(self, request, *args, **kwargs):
        super(LoginForm, self).__init__(request, *args, **kwargs)

        for fieldname in ['username', 'password']:
            self.fields[fieldname].label = ''
            self.fields[fieldname].help_text = None

        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control', 'autofocus': True, 'name': 'username', 'placeholder': 'Username'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password', 'placeholder': 'Password'})


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            'title',
            'description',
            'start_bid',
            'image_url',
            'tags'
        ]