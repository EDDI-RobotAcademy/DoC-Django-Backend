from abc import ABC, abstractmethod


class CartItemRepository(ABC):
    @abstractmethod
    def register(self, cartData, cart, product):
        pass

    @abstractmethod
    def findByCart(self, cart):
        pass

    @abstractmethod
    def findByProductId(self, productId):
        pass

    @abstractmethod
    def findAllByProductId(self, productId):
        pass

    @abstractmethod
    def findById(self, id):
        pass

    @abstractmethod
    def deleteByCartItemId(self, cartItemIdList):
        pass

    @abstractmethod
    def checkDuplication(self, cartItemList, productId):
        pass

