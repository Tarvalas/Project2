from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from .models import User, Listing
from .forms import RegisterForm, LoginForm, ListingForm, BiddingForm


def index(request):
    try:
        listings = Listing.objects.all()
    except Listing.DoesNotExist:
        listings = None
    return render(request, "auctions/index.html", {'listings': listings})


def login_view(request):
    form = LoginForm(request)
    if request.method == "POST":

        form = LoginForm(request, request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            # Check if authentication successful
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "auctions/login.html", {
                    "message": "Invalid username and/or password.",
                    "form": form
                })
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password.",
                "form": form
            }) 
    else:
        return render(request, "auctions/login.html", {
            "form": form
        }) 


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Attempt to create new user
            try:
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(request, username = username, password = password)
                form.save()
            except IntegrityError:
                return render(request, "auctions/register.html", {
                    "message": "Username already taken.",
                    "form": form
                })
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/register.html", {
                "message": "Form is not valid.",
                "form": form        
            })
    else:
        return render(request, "auctions/register.html", {
            "form": RegisterForm()
        })


def create_listing_view(request):
    form = ListingForm()

    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            try:
                form.instance.user = request.user
                form.save()
            except IntegrityError:
                return render(request, "auctions/listing_create.html", {
                    "message": "Error posting item.",
                    "form": form
                })
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/listing_create.html", {
                "message": "Error with form.",
                "form": form
            })
    else:
        return render(request, "auctions/listing_create.html", {
            "form": form
        })


def edit_listing_view(request, item_id):
    listing = Listing.objects.get(id=item_id)

    if request.method == "POST":
        form = ListingForm(request.POST, instance=listing)
        if form.is_valid():
            try:
                #form.instance.user = request.user
                form.save()
            except IntegrityError:
                return render(request, "auctions/listing_edit.html", {
                    "message": "Error updating item.",
                    "form": form
                })
            return HttpResponseRedirect(reverse("edit_listing", args=[item_id]))
        else:
            return render(request, "auctions/listing_edit.html", {
                "message": "Error with form.",
                "form": form
            })

    if listing.user != request.user:
        form = BiddingForm()
        return render(request, "auctions/listing.html", {
            "message": "You are not authorized to edit this listing.",
            "listing": listing,
            "form": form,
        })
    else:
        form = ListingForm(instance=listing)
        fields = ["title", "image_url"]
        return render(request, "auctions/listing_edit.html", {
            "listing": listing,
            "form": form,
            "fields": fields,
        })


def see_listing(request, item_id):
    if request.method == 'POST':
        form = BiddingForm(request.POST)
        if form.is_valid():
            listing = Listing.objects.get(id=item_id)
            if form.cleaned_data['current_bid'] > listing.current_bid:
                listing.current_bid = form.cleaned_data['current_bid']
                listing.save(update_fields=['current_bid'])
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "form": form,
                })
            else:
                return render(request, "auctions/listing.html", {
                    "message": "Your bid must be greater than the current bid.",
                    "listing": listing,
                    "form": form,
                })
    else:
        listing = Listing.objects.get(id=item_id)
        can_edit = listing.user == request.user
        form = BiddingForm()
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "form": form,
            "can_edit": can_edit,
        })