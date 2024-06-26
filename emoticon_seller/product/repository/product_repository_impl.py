import os
from product.entity.models import Product
from product.repository.product_repository import ProductRepository
from emoticon_seller import settings




class ProductRepositoryImpl(ProductRepository):
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def list(self):
        return Product.objects.all().order_by('productName')


    def create(self, productName, productPrice, writer, productCategory, content, productImage):
        uploadDirectory='../../DoC-Vue-Frontend/src/assets/images/uploadimages'
        print('업로드된 디렉토리 : ', uploadDirectory)
        os.makedirs(uploadDirectory, exist_ok=True)

        imagePath = os.path.join(uploadDirectory, productImage.name)
        with open(imagePath, 'wb+') as destination:
            for chunk in productImage.chunks():
                destination.write(chunk)
        print('이미지 경로: ',imagePath)

        product = Product(
            productName=productName,
            content=content,
            writer=writer,
            productPrice=productPrice,
            productCategory=productCategory,
            productImage=productImage.name
        )
        product.save()
        return product

    def findByProductId(self, productId):
        try:
            return Product.objects.get(productId=productId)
        except Product.DoesNotExist:
            return None

