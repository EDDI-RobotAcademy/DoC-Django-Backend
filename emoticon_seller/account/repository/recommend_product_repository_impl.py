from account.repository.recommend_product_repository import RecommendProductRepository
from account.entity.recommend_product import RecommendProduct

class RecommendProductRepositoryImpl(RecommendProductRepository):
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
    def create(self, recommendProductIdList, account):
        recommendProduct = RecommendProduct.objects.create(productIdList=recommendProductIdList, account=account)
        return recommendProduct

    def findByAccount(self, account):
        return RecommendProduct.objects.get(account=account)
