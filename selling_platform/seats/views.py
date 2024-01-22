from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from .permissions import IsOwnerOrAdmin
from .models import Stadium, Ticket, Seat, Match, Price
from .serializers import TicketSerializer, SeatSerializer, StadiumSerializer, MatchSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()

    def get_serializer_class(self):
        return TicketSerializer

    def get_permissions(self):
        if (self.action in ['reserve', 'cancel']) or (self.request.method in ['GET', 'OPTIONS']):
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.IsAdminUser()]

    @action(detail=True, methods=['put'])
    def reserve(self, request, pk=None):
        ticket = self.get_object()
        user = request.user

        with transaction.atomic():
            # Check if the ticket is available for reservation
            if ticket.status in [Ticket.EMPTY, Ticket.EXPIRED, Ticket.CANCELLED]:
                ticket.status = Ticket.RESERVED
                ticket.user = user
                ticket.save()

                return Response({'message': 'Ticket reserved successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Ticket is not available for reservation'},
                                status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def cancel(self, request, pk=None):
        ticket = self.get_object()
        user = request.user

        with transaction.atomic():
            # Check if the ticket is available for reservation
            if ticket.status in [Ticket.RESERVED] and user == ticket.user:
                ticket.status = Ticket.CANCELLED
                ticket.user = user
                ticket.save()

                return Response({'message': 'Ticket CANCELED successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Ticket is not available for cancellation'},
                                status=status.HTTP_400_BAD_REQUEST)


class StadiumViewSet(viewsets.ModelViewSet):
    queryset = Stadium.objects.all()
    serializer_class = StadiumSerializer
    permission_classes = [permissions.IsAdminUser]


class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [permissions.IsAdminUser]
