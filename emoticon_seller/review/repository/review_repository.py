from abc import ABC, abstractmethod


class ReviewRepository(ABC):
    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def register(self, reviewTitle, reviewWriter, reviewContent,reviewRating ,reviewImage, productId):
        pass

    @abstractmethod
    def findByReviewId(self, reviewId):
        pass

    @abstractmethod
    def update(self, review, reviewData):
        pass

    @abstractmethod
    def deleteByReviewID(self, reviewId):
        pass