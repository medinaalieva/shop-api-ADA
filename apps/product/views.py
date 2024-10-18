
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from apps.rating.serializers import RatingSerializer

from apps.product.models import Product
from apps.product.serializers import ProductSerializer, ProductListSerializer
from apps.product.permissions import IsOwnerOrAdmin, IsOwner


class StandartResultPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandartResultPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.request.method in ['PATCH', 'PUT', 'DELETE']:
            return [permissions.IsAuthenticated(), IsOwner()]
        return [permissions.IsAuthenticatedOrReadOnly()]

    @action(['GET', 'POST', 'PATCH', 'PUT', 'DELETE'], detail=True)
    def rating(self, request, pk):
        product = self.get_object()
        user = request.user

        if request.method == 'GET':
            ratings = product.ratings.all()
            serializer = RatingSerializer(ratings, many=True)
            return Response(serializer.data, 200)

        elif request.method == 'POST':
            serializer = RatingSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=user, product=product)
            return Response(serializer.data, 201)

        elif request.method in ['PUT', 'PATCH']:
            if not product.ratings.filter(owner=user).exists():
                return Response('Вы не оставляли рейтинг на этот товар', 404)
            rating = product.ratings.get(owner=user)
            serializer = RatingSerializer(rating, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, 200)

        else:
            if not product.ratings.filter(owner=user).exists():
                return Response('Вы не оставляли рейтинг на этот товар', 404)
            rating = product.ratings.get(owner=user)
            self.check_object_permissions(request, rating)
            rating.delete()
            return Response('Удалено', 204)
