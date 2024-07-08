from abc import ABC, abstractmethod


class ProductRepository(ABC):
    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def create(self, productName, productPrice, writer, productCategory, content, productTitleImage, productContentImage):
        pass

    @abstractmethod
    def findByProductId(self, productId):
        pass

    @abstractmethod
    def findAllByProductCategory(self, productCategory):
        pass