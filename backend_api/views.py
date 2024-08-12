from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Landlord, Listing, ListingType, Gallery
from .serializers import LandlordSerializer, ListingSerializer, ListingTypeSerializer, GallerySerializer

class LandlordListCreate(generics.ListCreateAPIView):
    queryset = Landlord.objects.all()
    serializer_class = LandlordSerializer
class LandlordRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Landlord.objects.all()
    serializer_class = LandlordSerializer
    lookup_field = 'pk'
    

class ListingTypeListCreate(generics.ListCreateAPIView):
    queryset = ListingType.objects.all()
    serializer_class = ListingTypeSerializer

class ListingListCreate(generics.ListCreateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class GalleryListCreate(generics.ListCreateAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
