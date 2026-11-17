from django.urls import path
from . import views

urlpatterns = [
    path("", views.feed, name="feed"),
    path("explore/", views.explore, name="explore"),
    path("like/<int:listing_id>/", views.toggle_like, name="toggle_like"),
    path("create/", views.create_listing, name="create_listing"),
    path("edit/<int:listing_id>/", views.edit_listing, name="edit_listing"),
    path("delete/<int:listing_id>/", views.delete_listing, name="delete_listing"),
    path("my-stall/", views.my_stall, name="my_stall"),
    path("stall/<int:user_id>/", views.user_stall, name="user_stall"),
    path("trade-offer/<int:listing_id>/", views.send_trade_offer, name="send_trade_offer"),
    path("trade-offers/", views.trade_offers, name="trade_offers"),
    path("trade-offer/<int:offer_id>/update/", views.update_trade_offer, name="update_trade_offer"),
    path("reset-feed/", views.reset_feed, name="reset_feed"),
]
