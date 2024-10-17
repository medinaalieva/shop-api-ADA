from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response

from apps.order.serializers import OrderSerializer


class CreateOrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        orders = user.orders.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=200)