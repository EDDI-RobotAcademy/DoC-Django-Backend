from abc import ABC, abstractmethod


class ReviewRepository(ABC):
    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def register(self, reviewTitle, reviewWriter, reviewContent,reviewRating ,reviewImage):
        pass

