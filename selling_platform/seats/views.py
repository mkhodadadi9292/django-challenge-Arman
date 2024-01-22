from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from .models import Ticket, Price
from .serializers import SeatSerializer


# from ..core.permissions import IsOwnerOrAdmin

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = SeatSerializer
