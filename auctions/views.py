from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.db.models import Max
from django.contrib.auth.decorators import login_required

from .models import User, Auctions, Bids, Comments, Watchlist

class createListingForm(forms.Form):
    lot = forms.CharField(label = "lot:")
    description = forms.CharField(label = "Desctription:", widget=forms.Textarea)
    url = forms.CharField(label = "url:", required = False)
    startBid = forms.IntegerField(label= "price:")
    category = forms.CharField(label= "Category:", required = False)

class bidForm(forms.Form):
    bid = forms.IntegerField(label= "bid:")

class commentForm(forms.Form):
    comment = forms.CharField(label = "comment:")

def index(request):
    auctions = Auctions.objects.exclude(closed = True)
    
    return render(request, "auctions/index.html", {
        "auctions": auctions
    })
                              

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='login')
def createListing(request):
    if request.method == 'POST':
        form = createListingForm(request.POST)
        if form.is_valid():
            cleanForm = form.cleaned_data

            if cleanForm['category'] == "":
                category = "None"
            else:
                category = cleanForm['category']

            auction = Auctions(
                lot = cleanForm['lot'],
                owner = request.user,
                url = cleanForm['url'],
                startBid = cleanForm['startBid'],
                currentBid = cleanForm['startBid'],
                description = cleanForm['description'],
                category = category
            )
            if auction.url == "":
                auction.url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/600px-No_image_available.svg.png"
            
            auction.save()
        
    return render(request, "auctions/createListing.html", {
        "form": createListingForm
    })


def listing(request, id):
    listing = Auctions.objects.get(id = id)
    status = listing.closed
    bids = Bids.objects.filter(lot = id)
    comments = Comments.objects.filter(lot = id)
    
    if status == True:
        maxBid = Bids.objects.filter(lot = id).aggregate(Max('bid'))
        winner = Bids.objects.get(lot = id, bid = maxBid['bid__max'])
        if request.user.is_authenticated:
            user = User.objects.get(username = request.user)
            watchlist = Watchlist.objects.filter(user = user, watchlist = id)
            data = list(watchlist)
            if data == []:
                watchlisted = 'Add to Watchlist'
            else:
                watchlisted = 'Watchlisted'
        else:
            watchlisted = 'Not logged in!'
        if str(winner.owner) == str(request.user):
            owner = True
        else:
            owner = False

        return render(request, "auctions/listingPage.html", {
            "auction": listing,
            "comments": comments,
            "bids": bids,
            "closed": status,
            "winner": winner.owner,
            "watchlist": watchlisted,
            "owner": owner
            
        })


    if request.user.is_authenticated:
        user = User.objects.get(username = request.user)
        watchlist = Watchlist.objects.filter(user = user, watchlist = id)
        data = list(watchlist)
        if data == []:
            watchlisted = 'Add to Watchlist'
        else:
            watchlisted = 'Watchlisted'

        if str(request.user) == str(listing.owner):
            owner = True
        else:
            owner = False



        if request.method == "POST":
            comment = commentForm(request.POST)
            if comment.is_valid():
                cleanedComment = comment.cleaned_data['comment']
                data_comment = Comments(
                    lot = id,
                    owner = request.user,
                    comment = cleanedComment
                )
                data_comment.save()



            bid = bidForm(request.POST)
            if bid.is_valid():
                cleanedBid = bid.cleaned_data['bid']
                maxBid = Bids.objects.filter(lot = id).aggregate(Max('bid'))
                if maxBid['bid__max'] is None:
                    neededBid = listing.startBid
                else:
                    neededBid = maxBid['bid__max'] + 1


                if cleanedBid >= neededBid:
                    data_bid = Bids(
                    lot = id,
                    owner = request.user,
                    bid = cleanedBid
                    )
                    data_bid.save()
                    maxBid_1 = Bids.objects.filter(lot = id).aggregate(Max('bid'))
                    listing.currentBid = maxBid_1['bid__max']
                    listing.save()
                else:
                    return render(request, "auctions/listingPage.html", {
                    "auction": listing,
                    "bidForm": bidForm,
                    "commentForm": commentForm,
                    "bids": bids,
                    "comments": comments,
                    "closed": status,
                    "message": "Incorrect value!",
                    "watchlist": watchlisted,
                    "owner": owner
                })

        return render(request, "auctions/listingPage.html", {
            "auction": listing,
            "bidForm": bidForm,
            "commentForm": commentForm,
            "comments": comments,
            "bids": bids,
            "watchlist": watchlisted,
            "closed": status,
            "owner": owner
        })
    else:
        return render(request, "auctions/listingPage.html", {
            "auction": listing,
            "bidForm": "Not logged in",
            "commentForm": "Not logged in",
            "comments": comments,
            "bids": bids,
            "watchlist": "Not logged in",
            "closed": status,
            "owner": False
        })

@login_required(login_url='login')
def addToWatchlist(request, id):
    print(id, "ID")
    user = request.user
    watchlist = Watchlist.objects.filter(user = user, watchlist = id)
    data = list(watchlist)
    if data == []:
        createWatchList = Watchlist(
            user = request.user,
            watchlist = id
        )
        createWatchList.save()
    else:
        watchlist.delete()

    return redirect('listing', id=id)
    
@login_required(login_url='login')
def watchlist(request):
    watchlist_id = Watchlist.objects.filter(user = request.user).values('watchlist')
    auctions = Auctions.objects.filter(id__in = watchlist_id).all()
    return render(request, "auctions/watchlist.html", {
        "auctions": auctions
    })
    
def categorys(request):
    categorys = Auctions.objects.all().values('category').distinct()
    return render(request, "auctions/category.html", {
        "categorys": categorys
    })

def categorys_listing(request, category):
    auctions = Auctions.objects.filter(category = category).all()
    return render(request, "auctions/index.html", {
        "auctions": auctions
    })

@login_required(login_url='login')
def close_auction(request, id):
    auction = Auctions.objects.get(id = id)
    if str(request.user) == str(auction.owner):
        auction.closed = True
        auction.save()
    else:
        HttpResponse("Error")
    return redirect('listing', id=id)
    