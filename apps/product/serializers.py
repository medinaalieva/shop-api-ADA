from rest_framework import serializers

from apps.category.models import Category
from apps.product.models import Product


class ProductParentSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        exclude = [
            'owner',
            'stock'
        ]

    def get_discounted_price(self, obj):
        if obj.discount is not None:
            discounted_price = obj.price - (obj.price * obj.discount / 100)
            return discounted_price
        return None


class ProductSerializer(ProductParentSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')
    owner_id = serializers.ReadOnlyField(source='owner.id')
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        exclude = [
            'owner',
            'stock'
        ]


class ProductListSerializer(ProductParentSerializer):
    class Meta:
        model = Product
        fields = ['id', 'image', 'title', 'discounted_price', 'price']


