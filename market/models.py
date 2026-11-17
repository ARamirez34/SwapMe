from django.db import models
from django.contrib.auth.models import User

class Listing(models.Model):
    TRADE = "TRADE"
    FREEBIE = "FREEBIE"
    POST_TYPES = [
        (TRADE, "Trade"),
        (FREEBIE, "Freebie"),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=120)
    description = models.TextField()
    image = models.ImageField(upload_to="listings/", blank=True, null=True)
    post_type = models.CharField(max_length=10, choices=POST_TYPES, default=TRADE)
    tags = models.CharField(max_length=200, blank=True, help_text="Space-separated tags")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.post_type})"

    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split() if tag.strip()]


class ListingLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_listings")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "listing")

    def __str__(self):
        return f"{self.user.username} liked {self.listing.title}"


class TradeOffer(models.Model):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    DECLINED = "DECLINED"
    
    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (ACCEPTED, "Accepted"),
        (DECLINED, "Declined"),
    ]

    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_offers")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_offers")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="trade_offers")
    offered_listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True, blank=True, 
                                       related_name="offered_in")
    message = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Trade offer from {self.from_user.username} to {self.to_user.username}"
