from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.createListing, name="createListing"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("addToWatchlist/<int:id>", views.addToWatchlist, name="addToWatchlist"),
    path("categorys", views.categorys, name="categorys"),
    path("categorys/<str:category>", views.categorys_listing, name="categorys_listing"),
    path("closeAuction/<int:id>", views.close_auction, name="closeAuction")
]
