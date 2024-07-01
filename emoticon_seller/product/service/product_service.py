from abc import ABC, abstractmethod

class ProductService(ABC):
    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def createProduct(self, productName, productPrice, writer, productCategory,content, productTitleImage,productContentImage):
        pass

    @abstractmethod
    def readProduct(self, productId):
        pass