from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from .models import User, Listing, Comment
from .forms import RegisterForm, LoginForm, ListingForm, BiddingForm, CommentForm


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
                user = form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(request, username = username, password = password)
 
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
        form = ListingForm(request.POST, is_edit=False)
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
                form.save()
            except IntegrityError:
                return render(request, "auctions/listing_edit.html", {
                    "message": "Error updating item.",
                    "form": form
                })
            return HttpResponseRedirect(reverse("see_listing", args=[item_id]))
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
    elif listing.num_bids > 0:
        return render(request, "auctions/listing.html", {
            "message": "You cannot edit a listing that already has bids.",
            "listing": listing,  
        })
    else:
        form = ListingForm(instance=listing)
        return render(request, "auctions/listing_edit.html", {
            "listing": listing,
            "form": form,
        })


def see_listing(request, item_id):
    listing = Listing.objects.get(id=item_id)
    bid_form = BiddingForm()
    can_edit = listing.user == request.user
    comments =listing.comments.all()
    comment_form = CommentForm()
    context = {
        "message": None,
        "listing": listing,
        "bid_form": bid_form,
        "can_edit": can_edit,
        "comments": comments,
        "comment_form": comment_form,
        "is_watchlist": False
    }
    if request.method == 'POST':
        if "bidding" in request.POST:
            bid_form = BiddingForm(request.POST)
            if bid_form.is_valid():
                if bid_form.cleaned_data['bid'] > listing.start_bid:            
                    listing.start_bid = bid_form.cleaned_data['bid']
                    listing.num_bids += 1
                    listing.save(update_fields=['start_bid', 'num_bids'])
                    return render(request, "auctions/listing.html", context)
                else:
                    context["message"] = "Your bid must be greater than the current bid."
                    return render(request, "auctions/listing.html", context=context)
        if "commenting" in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                if comment_form.cleaned_data["comment"]:
                    comment_form.instance.user = request.user
                    comment_form.instance.item = listing
                    comment_form.save()
                    return render(request, "auctions/listing.html", context=context)
                else:
                    context["message"] = "Your bid must be greater than the current bid."
                    return render(request, "auctions/listing.html", context=context)
    else:
        return render(request, "auctions/listing.html", context=context)


def watchlist_view(request):
    if request.method == "POST":
        if "add" in request.POST:
            request.user.watchlist.add(Listing.objects.get(id=int(request.POST["add"])))
            request.user.num_watchlist += 1
            request.user.save()
        else:
            request.user.watchlist.remove(Listing.objects.get(id=int(request.POST["remove"])))
            request.user.num_watchlist -= 1
            request.user.save()
    watchlist = request.user.watchlist.all()

    context = {
        "is_watchlist": True,
        "listings": watchlist
    }
    return render(request, "auctions/index.html", context=context)