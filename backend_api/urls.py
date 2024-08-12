from django.urls import path
from . import views

urlpatterns = [
    path("gallery/", views.GalleryListCreate.as_view(), name='gallery-list-create'),
    path("landlords/", views.LandlordListCreate.as_view(), name='landlord-list-create'),
    path("landlords/<int:pk>", views.LandlordRetrieveUpdateDelete.as_view(), name='update-delete'),
    path("listing/", views.ListingListCreate.as_view(), name="listing-list-create"),
    path("listing-type/", views.ListingTypeListCreate.as_view(), name="listingtype-list-create"),
]