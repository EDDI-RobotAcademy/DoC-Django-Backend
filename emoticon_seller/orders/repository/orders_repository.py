from abc import abstractmethod, ABC


class OrdersRepository(ABC):
    @abstractmethod
    def create(self, account):
        pass


