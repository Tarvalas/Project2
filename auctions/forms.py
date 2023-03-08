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
    def __init__(self, *args, is_edit=False, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)

        for fieldname in ['image_url', 'category']:
            self.fields[fieldname].required = False
        
        self.fields['title'].widget = forms.TextInput(attrs={'class': 'form-control', 'autofocus': True, 'name': 'title', 'placeholder':'Enter Title'})
        self.fields['description'].widget = forms.Textarea(attrs={'class': 'form-control', 'name': 'description', 'placeholder':'Enter Item Description'})
        self.fields['start_bid'].widget = forms.NumberInput(attrs={'step': 0.01, 'class': 'form-control', 'name': 'start_bid', 'placeholder':'Enter Starting Bid'})
        self.fields['image_url'].widget = forms.URLInput(attrs={'class': 'form-control', 'name': 'image_url', 'placeholder':'Enter Image URL'})
        self.fields['category'].widget = forms.TextInput(attrs={'class': 'form-control', 'name': 'category', 'placeholder':'Enter Category Name'})

    class Meta:
        model = Listing
        fields = [
            'title',
            'description',
            'start_bid',
            'image_url',
            'category',
        ]


class BiddingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BiddingForm, self).__init__(*args, **kwargs)
        self.fields['bid'].required = True

        self.fields['bid'].widget = forms.NumberInput(attrs={'step': 0.01, 'class': 'form-control', 'name': 'bid', 'placeholder':'Enter Bid'})
    
    class Meta:
        model = Bid
        fields = [
            'bid'
        ]

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

        self.fields["comment"].help_text = "Your comment must be limited to 3000 characters."
        self.fields["comment"].label = ''
        self.fields["comment"].widget = forms.Textarea(attrs={'class': 'form-control enter-comment', 'name': 'comment', 'placeholder':'Enter a comment...'})
    
    class Meta:
        model = Comment
        fields = [
            'comment'
        ]
