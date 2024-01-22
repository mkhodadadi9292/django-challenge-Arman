from django.shortcuts import get_object_or_404
from celery import shared_task
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from .permissions import IsOwnerOrAdmin
from .models import Stadium, Ticket, Seat, Match, Price
from .serializers import PriceSerializer, TicketSerializer, SeatSerializer, StadiumSerializer, MatchSerializer


#
@shared_task
def convert_reserved_to_empty(ticket_id):
    try:
        # Get the ticket
        ticket = Ticket.objects.get(id=ticket_id)
        # Check if the ticket is still in the reserved state
        if ticket.status == 'Reserved':
            # Change the status to 'Empty'
            ticket.status = 'Empty'
            ticket.save()

    except Ticket.DoesNotExist:
        # Handle the case where the ticket no longer exists
        pass


def initiate_conversion(ticket_id):
    transaction.on_commit(lambda: convert_reserved_to_empty.apply_async((ticket_id,), countdown=300))


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
                # Following function will run in background in order to convert the reserved ticket to EMPTY status
                # (ticket are not available for reservation)
                # initiate_conversion(ticket.id)

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

    # permission_classes = [permissions.IsAdminUser]
    def get_permissions(self):
        if self.request.method in ['GET', 'OPTIONS']:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.IsAdminUser()]


class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

    def get_permissions(self):
        if self.request.method in ['GET', 'OPTIONS']:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.IsAdminUser()]


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    def get_permissions(self):
        if self.request.method in ['GET', 'OPTIONS']:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.IsAdminUser()]


class PriceViewSet(viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer

    def get_permissions(self):
        if self.request.method in ['GET', 'OPTIONS']:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.IsAdminUser()]
