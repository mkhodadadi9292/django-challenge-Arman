from rest_framework import serializers
from .models import Price, Seat


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'status', 'price', 'user']
