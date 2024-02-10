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
from celery.exceptions import Ignore
from django.db.models import F
import logging
logger = logging.getLogger(__name__)
#
import time
@shared_task
def convert_reserved_to_empty(ticket_id):
    logger.debug("convert_reserved_to_empty is started. ticket_id={0}".format(ticket_id))
    try:
        # Get the ticket
        ticket = Ticket.objects.get(id=ticket_id)
        # Check if the ticket is still in the reserved state

        logger.info(f"Ticket => status={ticket.status}")
        if ticket.status == Ticket.RESERVED:
            # Change the status to 'Empty'
            ticket.status = Ticket.EMPTY
            ticket.save()
            print(f"Ticket status after applying some changes to database => {ticket.status}")
            print("convert_reserved_to_empty is finished. ticket_id={0}".format(ticket_id))
            print("-"*25)
        else:
            logger.info(f"current ticket.status = {ticket.status}")
            logger.info(f"target Ticket.RESERVED = {Ticket.RESERVED}")
    except Ticket.DoesNotExist:
        logger.warning(f"Ticket with ID {ticket_id} does not exist")

    # try:
    #     # Atomically update the ticket status if it is still in the reserved state
    #     Ticket.objects.filter(id=ticket_id, status=Ticket.RESERVED).update(status=Ticket.EMPTY)
    #     logger.info("Ticket status successfully updated to 'Empty'")
    # except Ticket.DoesNotExist:
    #     logger.warning(f"Ticket with ID {ticket_id} does not exist")
    # except Exception as e:
    #     logger.error(f"Error updating ticket status: {e}")

def initiate_conversion(ticket_id):
    # transaction.on_commit(lambda: convert_reserved_to_empty.delay(ticket_id))
    convert_reserved_to_empty.apply_async(args=[ticket_id], countdown=10)
    # transaction.on_commit(lambda: convert_reserved_to_empty.apply_async((ticket_id,), countdown=20))
    # convert_reserved_to_empty.apply_async(args=[ticket_id], countdown=10)
    # transaction.on_commit(lambda: task_send_welcome_email.delay(user.pk))


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

                initiate_conversion(ticket.id)
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
