from abc import ABC, abstractmethod


class ReportRepository(ABC):
    @abstractmethod
    def findByAccount(self, account):
        pass
    @abstractmethod
    def register(self, account, age, gender):
        pass