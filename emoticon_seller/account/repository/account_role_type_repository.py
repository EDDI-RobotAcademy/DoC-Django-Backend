from abc import ABC, abstractmethod


class AccountRoleTypeRepository(ABC):
    @abstractmethod
    def findRoleTypeById(self, roleTypeId):
        pass