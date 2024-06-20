from abc import ABC,abstractmethod

class ProfileRepository(ABC):

    @abstractmethod
    def findByemail(self,email):
        pass