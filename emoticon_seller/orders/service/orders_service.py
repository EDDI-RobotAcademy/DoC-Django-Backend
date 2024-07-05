from abc import ABC, abstractmethod


class OrdersService(ABC):
    @abstractmethod
    def createCartOrder(self, account, orderItemList):
        pass

    @abstractmethod
    def createProductOrder(self, account, orderItem):
        pass

    @abstractmethod
    def getAllOrders(self):
        pass

    @abstractmethod
    def findAllByAccountId(self, accountId):
        pass