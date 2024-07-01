from abc import ABC, abstractmethod


class ReviewService(ABC):
    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def registerReview(self, reviewTitle, reviewWriter, reviewContent,reviewRating,reviewImage):
        pass

