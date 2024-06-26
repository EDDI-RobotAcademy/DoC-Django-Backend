from rest_framework import serializers

from product.entity.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['productId', 'productName', 'productPrice', 'productImage', 'productCategory','writer', 'content', 'regDate', 'updDate']
        read_only_fields = ['regDate', 'updDate']
