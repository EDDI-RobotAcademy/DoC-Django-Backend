from review.repository.review_repository_impl import ReviewRepositoryImpl
from review.service.review_service import ReviewService


class ReviewServiceImpl(ReviewService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__reviewRepository = ReviewRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def list(self):
        return self.__reviewRepository.list()

    def registerReview(self, reviewTitle, reviewWriter, reviewContent,reviewRating,reviewImage):
        return self.__reviewRepository.register(reviewTitle, reviewWriter, reviewContent,reviewRating,reviewImage)

    def readReview(self, reviewId):
        return self.__reviewRepository.findByReviewId(reviewId)

    def updateReview(self, reviewId, reviewData):
        review = self.__reviewRepository.findByReviewId(reviewId)
        return self.__reviewRepository.update(review, reviewData)

    def removeReview(self, reviewId):
        return self.__reviewRepository.deleteByReviewID(reviewId)