from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Stadium, Seat, Match, Price, Ticket
from django.db import transaction


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class StadiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stadium
        fields = '__all__'


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'

    def validate(self, data):
        """
        Validate that there is no overlapping interval time for matches in the same stadium.
        """
        stadium = data['stadium']
        start_time = data['start_time']
        end_time = data['end_time']

        overlapping_matches = Match.objects.filter(
            stadium__id=stadium[0].id,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exclude(pk=self.instance.pk if self.instance else None)

        if overlapping_matches.exists():
            raise serializers.ValidationError('Overlapping interval time with existing matches in the same stadium.')

        return data
