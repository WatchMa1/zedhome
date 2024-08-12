# myapp/serializers.py
from rest_framework import serializers
from .models import Landlord, Listing, ListingType, Gallery

class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'

class LandlordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Landlord
        fields = '__all__'

class ListingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingType
        fields = '__all__'

class ListingSerializer(serializers.ModelSerializer):
    gallery = GallerySerializer(many=True, read_only=True)

    class Meta:
        model = Listing
        fields = '__all__'
