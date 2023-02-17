from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import User, Listing, Bid, Comment
from taggit.forms import TagWidget


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
    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)

        for fieldname in ['image_url', 'tags']:
            self.fields[fieldname].required = False

        self.fields['title'].widget = forms.TextInput(attrs={'class': 'form-control', 'autofocus': True, 'name': 'title', 'placeholder':'Enter Title'})
        self.fields['description'].widget = forms.Textarea(attrs={'class': 'form-control', 'name': 'description', 'placeholder':'Enter Item Description'})
        self.fields['start_bid'].widget = forms.NumberInput(attrs={'step': 0.01, 'class': 'form-control', 'name': 'start_bid', 'placeholder':'Enter Starting Bid'})
        self.fields['image_url'].widget = forms.URLInput(attrs={'class': 'form-control', 'name': 'image_url', 'placeholder':'Enter Image URL'})
        self.fields['tags'].widget = TagWidget(attrs={'class': 'form-control', 'name': 'tags', 'placeholder':'Enter Item Tags'})

    class Meta:
        model = Listing
        fields = [
            'title',
            'description',
            'start_bid',
            'image_url',
            'tags',
        ]