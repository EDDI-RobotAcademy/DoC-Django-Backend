from abc import abstractmethod, ABC


class OrdersRepository(ABC):
    @abstractmethod
    def create(self, account):
        pass

    @abstractmethod
    def getAllOrders(self):
        pass

    @abstractmethod
    def findAllByAccountId(self, accountId):
        pass

