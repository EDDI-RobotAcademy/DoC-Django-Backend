from abc import ABC,abstractmethod

class ProfileRepository(ABC):

    @abstractmethod
    def findByemail(self,email):
        pass

    @abstractmethod
    def findBynickname(self,nickname):
        pass

    @abstractmethod
    def create(self,nickname,email,account):
        pass