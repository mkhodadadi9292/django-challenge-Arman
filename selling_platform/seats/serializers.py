from rest_framework import serializers
from .models import Price, Ticket


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'status', 'price', 'user']
