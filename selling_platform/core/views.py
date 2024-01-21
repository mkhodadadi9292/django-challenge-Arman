from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    ListModelMixin
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Wallet
from .serializers import WalletOnlyReadSerializer, WalletOnlyWriteSerializer
from .permissions import IsOwnerOrAdmin


class WalletViewSet(ListModelMixin,
                    RetrieveModelMixin,
                    UpdateModelMixin,
                    CreateModelMixin,
                    GenericViewSet):
    queryset = Wallet.objects.select_related('user').all()

    # permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return WalletOnlyWriteSerializer
        return WalletOnlyReadSerializer

    def get_permissions(self):
        if (self.action in ['charge', 'withdraw']) or (self.request.method in ['GET']):
            return [IsOwnerOrAdmin()]
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return [IsAdminUser()]
        else:
            return [IsOwnerOrAdmin()]

    # permission_classes
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
    def withdraw(self, request, pk=None):
        wallet = self.get_object()
        self.check_object_permissions(request, wallet)

        amount = request.data.get('money', 0)
        if wallet.money >= amount:
            wallet.money -= amount
            wallet.save()
            return Response({'message': f'Wallet withdrawn by {amount}', 'new_balance': wallet.money},
                            status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)
