from rest_framework import serializers
from .models import Price, Seat

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'title', 'products_count']