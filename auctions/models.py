from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Watchlist(models.Model):
    user = models.CharField(max_length=64)
    watchlist = models.CharField(max_length=64, blank = True)
    def __str__(self):
        return f"{self.user}: {self.watchlist}"

class Bids(models.Model):
    lot = models.CharField(max_length=64)
    owner = models.CharField(max_length=64)
    bid = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lot}: {self.owner}, {self.bid}, {self.time}"

    
class Comments(models.Model):
    lot = models.CharField(max_length=64)
    owner = models.CharField(max_length=64)
    comment = models.CharField(max_length=256)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lot}: {self.owner}, {self.comment}, {self.time}"

class Auctions(models.Model):
    lot = models.CharField(max_length=64)
    owner = models.CharField(max_length=64)
    url = models.CharField(max_length=256, blank = True)
    startBid = models.IntegerField()
    currentBid = models.IntegerField()
    description = models.CharField(max_length=256)
    category = models.CharField(max_length=64, blank = True)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.lot}: {self.owner}, {self.startBid}, {self.description}, {self.category}, {self.url}"





