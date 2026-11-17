from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Listing, ListingLike, TradeOffer
from .forms import ListingForm
from django.contrib.auth.models import User

@login_required(login_url="login")
def feed(request):
    # Get all listings except user's own
    listings = Listing.objects.exclude(owner=request.user).order_by("-created_at")
    
    # Get liked listings for current user
    liked_listing_ids = ListingLike.objects.filter(user=request.user).values_list("listing_id", flat=True)
    
    context = {
        "listings": listings,
        "liked_listing_ids": list(liked_listing_ids),
    }
    return render(request, "market/feed.html", context)


@login_required(login_url="login")
def toggle_like(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    
    like_obj, created = ListingLike.objects.get_or_create(user=request.user, listing=listing)
    
    if not created:
        like_obj.delete()
        liked = False
    else:
        liked = True
    
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"liked": liked})
    
    return redirect("feed")


@login_required(login_url="login")
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            messages.success(request, "Listing created successfully!")
            return redirect("my_stall")
    else:
        form = ListingForm()
    
    return render(request, "market/create_listing.html", {"form": form})


@login_required(login_url="login")
def edit_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id, owner=request.user)
    
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, "Listing updated successfully!")
            return redirect("my_stall")
    else:
        form = ListingForm(instance=listing)
    
    return render(request, "market/edit_listing.html", {"form": form, "listing": listing})


@login_required(login_url="login")
def delete_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id, owner=request.user)
    
    if request.method == "POST":
        listing.delete()
        messages.success(request, "Listing deleted successfully!")
        return redirect("my_stall")
    
    return render(request, "market/delete_listing.html", {"listing": listing})


@login_required(login_url="login")
def my_stall(request):
    listings = Listing.objects.filter(owner=request.user).order_by("-created_at")
    liked_listings = Listing.objects.filter(likes__user=request.user).order_by("-likes__created_at")
    
    context = {
        "listings": listings,
        "liked_listings": liked_listings,
    }
    return render(request, "market/my_stall.html", context)


@login_required(login_url="login")
def user_stall(request, user_id):
    user = get_object_or_404(User, id=user_id)
    listings = Listing.objects.filter(owner=user).order_by("-created_at")
    
    context = {
        "stall_user": user,
        "listings": listings,
    }
    return render(request, "market/user_stall.html", context)


@login_required(login_url="login")
def send_trade_offer(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    
    if request.method == "POST":
        offered_listing_id = request.POST.get("offered_listing_id")
        message = request.POST.get("message", "")
        
        offered_listing = None
        if offered_listing_id:
            offered_listing = get_object_or_404(Listing, id=offered_listing_id, owner=request.user)
        
        trade_offer = TradeOffer.objects.create(
            from_user=request.user,
            to_user=listing.owner,
            listing=listing,
            offered_listing=offered_listing,
            message=message,
        )
        
        messages.success(request, "Trade offer sent!")
        return redirect("feed")
    
    user_listings = Listing.objects.filter(owner=request.user)
    context = {
        "listing": listing,
        "user_listings": user_listings,
    }
    return render(request, "market/send_trade_offer.html", context)


@login_required(login_url="login")
def trade_offers(request):
    offers = TradeOffer.objects.filter(to_user=request.user).order_by("-created_at")
    
    context = {
        "offers": offers,
    }
    return render(request, "market/trade_offers.html", context)


@login_required(login_url="login")
def update_trade_offer(request, offer_id):
    offer = get_object_or_404(TradeOffer, id=offer_id, to_user=request.user)
    
    if request.method == "POST":
        action = request.POST.get("action")
        
        if action == "accept":
            offer.status = TradeOffer.ACCEPTED
        elif action == "decline":
            offer.status = TradeOffer.DECLINED
        
        offer.save()
        messages.success(request, f"Trade offer {action}ed!")
        return redirect("trade_offers")
    
    return render(request, "market/update_trade_offer.html", {"offer": offer})


@login_required(login_url="login")
def reset_feed(request):
    """Reset all likes/dislikes for the current user"""
    ListingLike.objects.filter(user=request.user).delete()
    messages.success(request, "Feed reset! You can now go through all listings again.")
    return redirect("feed")


@login_required(login_url="login")
def explore(request):
    """Explore and search listings"""
    search_query = request.GET.get('q', '').strip()
    filter_type = request.GET.get('type', '').strip()
    
    # Start with all listings except user's own
    listings = Listing.objects.exclude(owner=request.user).order_by("-created_at")
    
    # Apply search filter
    if search_query:
        listings = listings.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(tags__icontains=search_query)
        )
    
    # Apply post type filter
    if filter_type in ['TRADE', 'FREEBIE']:
        listings = listings.filter(post_type=filter_type)
    
    # Get liked listings for current user
    liked_listing_ids = ListingLike.objects.filter(user=request.user).values_list("listing_id", flat=True)
    
    context = {
        "listings": listings,
        "liked_listing_ids": list(liked_listing_ids),
        "search_query": search_query,
        "filter_type": filter_type,
    }
    return render(request, "market/explore.html", context)
