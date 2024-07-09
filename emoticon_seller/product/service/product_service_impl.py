import random

from product.repository.product_repository_impl import ProductRepositoryImpl
from product.service.product_service import ProductService

class ProductServiceImpl(ProductService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__productRepository = ProductRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def list(self):
        return self.__productRepository.list()

    def createProduct(self, productName, productPrice, writer, productCategory, content, productTitleImage,productContentImage):
        return self.__productRepository.create(productName, productPrice, writer, productCategory, content, productTitleImage,productContentImage)

    def readProduct(self, productId):
        return self.__productRepository.findByProductId(productId)

    def randomList(self, productCategory):
        productByCategory = self.__productRepository.findAllByProductCategory(productCategory)
        randomNumbers = random.sample(range(0, 33), 4)
        productByRandomNumbers = [productByCategory[idx] for idx in randomNumbers]
        return productByRandomNumbers

    def recommendList(self, recommendProductIdList):
        return self.__productRepository.findByProdictIdList(recommendProductIdList)

