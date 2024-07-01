from abc import ABC, abstractmethod


class ReviewRepository(ABC):
    @abstractmethod
    def list(self):
        pass
