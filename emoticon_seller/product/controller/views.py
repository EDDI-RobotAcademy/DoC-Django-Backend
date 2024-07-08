import random

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from product.entity.models import Product
from product.serializers import ProductSerializer
from product.service.product_service_impl import ProductServiceImpl

class ProductView(viewsets.ViewSet):
    queryset = Product.objects.all()
    productService = ProductServiceImpl.getInstance()

    def list(self, request):
        productList = self.productService.list()
        # print('productList : ', productList)
        serializer = ProductSerializer(productList, many=True)
        return Response(serializer.data)

    def register(self, request):
        try:
            data = request.data

            productTitleImage = request.FILES.get('productTitleImage')
            productContentImage = request.FILES.get('productContentImage')
            productName = data.get('productName')
            productPrice = data.get('productPrice')
            writer = data.get('writer')
            productCategory = data.get('productCategory')
            content = data.get('content')
            # print('writer가 잘 들어왔는지 확인 : ', writer)
            # print('productTitleImage: ', productTitleImage.name)
            # print('productContentImage: ', productContentImage.name)

            

            if not all([productName, productPrice, writer, productCategory, content, productTitleImage,productContentImage]):
                return Response({'error': '모든 내용을 채워주세요!'},
                                status=status.HTTP_400_BAD_REQUEST)

            self.productService.createProduct(productName, productPrice, writer, productCategory, content, productTitleImage, productContentImage)

            serializer = ProductSerializer(data=request.data)
            return Response(status=status.HTTP_200_OK)

        except Exception as e:
            print('상품 등록 과정 중 문제 발생:', e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def readProduct(self, request, pk=None):
        product = self.productService.readProduct(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def randomProductList(self, request):
        productCategory = request.query_params.get('productCategory')
        productByRandomNumbers = self.productService.randomList(productCategory)
        serializer = ProductSerializer(productByRandomNumbers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)