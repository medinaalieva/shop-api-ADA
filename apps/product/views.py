from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend

from apps.rating.serializers import RatingSerializer

from apps.product.models import Product
from apps.product.serializers import ProductSerializer, ProductListSerializer
from apps.product.permissions import IsOwnerOrAdmin, IsOwner


class StandartResultPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'


class ProductViewSet(ModelViewSet)