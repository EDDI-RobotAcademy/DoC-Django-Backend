from abc import ABC, abstractmethod


class RecommendProductRepository(ABC):
    @abstractmethod
    def create(self, recommendProductIdList, account):
        pass

    @abstractmethod
    def findByAccount(self, account):
        pass

