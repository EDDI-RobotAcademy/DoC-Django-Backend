from abc import abstractmethod, ABC


class OrdersItemRepository(ABC):
    @abstractmethod
    def create(self, orders, product, price):
        pass

    @abstractmethod
    def findAllByOrdersId(self, ordersId):
        pass

    @abstractmethod
    def checkDuplication(self, allOrdersItemList, productId):
        pass
