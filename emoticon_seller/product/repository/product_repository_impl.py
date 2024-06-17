import os
from product.entity.models import Product
from product.repository.product_repository import ProductRepository
# from emoticon_seller import settings



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


    def create(self, productName, productPrice, writer, content, productImage):
        uploadDirectory='../../DoC-Vue-Frontend/src/assets/images/uploadimages' # 안되면 고치기
        os.makedirs(uploadDirectory, exist_ok=True)

        imagePath = os.path.join(uploadDirectory, productImage.name)
        with open(imagePath, 'wb+') as destination:
            for chunk in productImage.chunks():
                destination.write(chunk)

        product = Product(
            productName=productName,
            content=content,
            writer=writer,
            productPrice =productPrice,
            productImage=productImage.name
        )
        product.save()
        return product





