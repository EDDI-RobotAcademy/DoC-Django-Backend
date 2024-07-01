import os

from review.entity.models import Review
from review.repository.review_repository import ReviewRepository
from emoticon_seller import settings


class ReviewRepositoryImpl(ReviewRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def list(self):
        return Review.objects.all().order_by('reviewRegDate')
