from rest_framework import viewsets, status
from rest_framework.response import Response

from account.repository.account_role_type_repository_impl import AccountRoleTypeRepositoryImpl
from account.repository.profile_repository_impl import ProfileRepositoryImpl
from account.repository.recommend_product_repository_impl import RecommendProductRepositoryImpl
from account.serializers import AccountSerializer
from account.service.account_service_impl import AccountServiceImpl
from emoticon_seller import settings
from oauth.service.redis_service_impl import RedisServiceImpl


class AccountView(viewsets.ViewSet):
    accountService = AccountServiceImpl.getInstance()
    redisService = RedisServiceImpl.getInstance()
    profileRepository = ProfileRepositoryImpl.getInstance()
    accountRoleTypeRepository = AccountRoleTypeRepositoryImpl.getInstance()
    recommendProductRepository = RecommendProductRepositoryImpl.getInstance()

    def checkEmailDuplication(self, request):
        # url = self.oauthService.kakaoLoginAddress()
        print("checkEmailDuplication()")

        try:
            email = request.data.get('email')
            isDuplicate = self.accountService.checkEmailDuplication(email)

            return Response({'isDuplicate': isDuplicate, 'message': 'Email이 이미 존재' \
                             if isDuplicate else 'Email 사용 가능'}, status=status.HTTP_200_OK)
        except Exception as e:
            print("이메일 중복 체크 중 에러 발생:", e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def checkNicknameDuplication(self, request):
        print("checkNicknameDuplication()")

        try:
            nickname = request.data.get('newNickname')
            print(f"nickname: {nickname}")
            isDuplicate = self.accountService.checkNicknameDuplication(nickname)

            return Response({'isDuplicate': isDuplicate, 'message': 'Nickname이 이미 존재' \
                             if isDuplicate else 'Nickname 사용 가능'}, status=status.HTTP_200_OK)
        except Exception as e:
            print("닉네임 중복 체크 중 에러 발생:", e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def registerAccount(self, request):
        try:
            nickname = request.data.get('nickname')
            email = request.data.get('email')
            isAdmin = request.data.get('isAdmin')
            isBusiness = request.data.get('isBusiness')

            if isAdmin:
                roleType = 'ADMIN'
            elif isBusiness:
                roleType = 'SELLER'
            else:
                roleType = 'CUSTOMER'


            account = self.accountService.registerAccount(
                loginType='KAKAO',
                roleType=roleType,
                nickname=nickname,
                email=email
            )

            serializer = AccountSerializer(account)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("계정 생성 중 에러 발생:", e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def getNickname(self, request):
        userToken = request.data.get('userToken')
        if not userToken:
            return Response(None, status=status.HTTP_200_OK)
        # print(f"userToken: {userToken}")
        accountId = self.redisService.getValueByKey(userToken)
        # print(f"accountId: {accountId}")
        profile = self.profileRepository.findById(accountId)
        # print(f"profile: {profile}")
        nickname = profile.nickname
        return Response(nickname, status=status.HTTP_200_OK)

    def getRoleType(self, request):
        userToken = request.data.get('userToken')
        if not userToken:
            return Response(None, status=status.HTTP_200_OK)
        # print(f"userToken: {userToken}")
        accountId = self.redisService.getValueByKey(userToken)
        # print(f"accountId: {accountId}")
        account = self.accountService.findAccountById(accountId)
        print(f"account: {account}")
        accountRoleTypeId = account.roleType_id
        roleType = self.accountRoleTypeRepository.findRoleTypeById(accountRoleTypeId)
        return Response(roleType, status=status.HTTP_200_OK)

    def getAdminPassword(self, request):
        correctAdminPassword = settings.ADMIN_PASSWORD
        return Response(correctAdminPassword, status=status.HTTP_200_OK)

    def registerRecommend(self, request):
        userToken = request.data.get('userToken')
        accountId = self.redisService.getValueByKey(userToken)
        account = self.accountService.findAccountById(accountId)
        recommendProductIdList = request.data.get('recommendProductIdList')
        print(f"recommendProductIdList: {recommendProductIdList}")
        self.recommendProductRepository.create(recommendProductIdList, account)

        return Response(status=status.HTTP_200_OK)

    def recommendProductIdList(self, request):
        userToken = request.data.get('userToken')
        accountId = self.redisService.getValueByKey(userToken)
        account = self.accountService.findAccountById(accountId)
        recommendProduct = self.recommendProductRepository.findByAccount(account)
        recommendProductIdList = recommendProduct.productIdList

        return Response(recommendProductIdList, status=status.HTTP_200_OK)


