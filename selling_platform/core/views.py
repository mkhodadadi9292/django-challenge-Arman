from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Sum
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    ListModelMixin
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Wallet, TransactionHistory
from .serializers import WalletOnlyReadSerializer, WalletOnlyWriteSerializer
from .permissions import IsOwnerOrAdmin
from seats.models import Seat


#
# def get_queryset(self):
#     user = self.request.user
#
#     if user.is_staff:
#         return Order.objects.all()
#
#     customer_id = Customer.objects.only(
#         'id').get(user_id=user.id)
#     return Order.objects.filter(customer_id=customer_id)


class WalletViewSet(ListModelMixin,
                    RetrieveModelMixin,
                    UpdateModelMixin,
                    CreateModelMixin,
                    GenericViewSet):
    queryset = Wallet.objects.select_related('user').all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return WalletOnlyWriteSerializer
        return WalletOnlyReadSerializer

    def get_permissions(self):
        if (self.action in ['purchase', 'charge']) or (self.request.method in ['GET', 'OPTIONS']):
            return [IsOwnerOrAdmin()]
        else:
            return [IsAdminUser()]

    @action(detail=True, methods=['post'])
    def charge(self, request, pk=None):
        wallet = self.get_object()
        self.check_object_permissions(request, wallet)
        # TODO: much better to handle inside the related serializer.
        amount = request.data.get('money', 0)
        wallet.money += amount
        wallet.save()

        return Response({'message': f'Wallet charged by {amount}', 'new_balance': wallet.money},
                        status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def purchase(self, request, pk=None):
        wallet = self.get_object()
        self.check_object_permissions(request, wallet)

        try:
            with transaction.atomic():
                # Fetch reserved seats for the user
                reserved_seats = Seat.objects.filter(user=request.user, status=Seat.RESERVED)

                # Step 1: Calculate the total price of RESERVED seats owned by the user
                total_price_reserved_seats = reserved_seats.aggregate(total_price=Sum('price__unit_price'))[
                                                 'total_price'] or 0

                # Step 2: Deduct the total price from the wallet
                if wallet.money >= total_price_reserved_seats:
                    wallet.money -= total_price_reserved_seats
                    wallet.save()
                else:
                    raise ValueError('Insufficient funds in the wallet')

                # Step 3: Change the status of RESERVED seats to CONFIRMED
                Seat.objects.filter(user=request.user, status=Seat.RESERVED).update(status=Seat.CONFIRMED)

                # Step 4: Log the transaction history
                transaction_records = TransactionHistory.objects.create(
                    amount=total_price_reserved_seats,
                    user=request.user
                )
                transaction_records.seats.set(reserved_seats.all())

                return Response({'message': 'Purchase successful'}, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
