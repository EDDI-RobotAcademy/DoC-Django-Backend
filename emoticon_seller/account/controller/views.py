from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.response import Response

from account.service.account_service_impl import AccountServiceImpl

class AccountView(viewsets.ViewSet):

    accountService = AccountServiceImpl.getInstance()

    def checkEmailDuplication(self,request):
        print('checkEmailDuplication')

        try:
            email = request.data.get('email')
            isDuplicate = self.accountService.checkEmailDuplication(email)

            return Response({'isDuplicate': isDuplicate, 'message': 'email이 이미 있습니다.'\
                             if isDuplicate else 'email이 사용 가능합니다.'},status=status.HTTP_200_OK)
        except Exception as e:
            print('이메일 중복체크 중 오류 발생:',e)
            return Response({'error': str(e)},status=status.HTTP_400_BAD_REQUEST)

    def checkNicknameDuplication(self,request):
        print("checkNicknameDuplication()")

        try:
            nickname = request.data.get('newNickname')
            print(f"nickname: {nickname}")
            isDuplicate = self.accountService.checkEmailDuplication(nickname)

            return Response({'isDuplicate': isDuplicate, 'message': 'Nickname이 이미 존재' \
                if isDuplicate else 'Nickname 사용 가능'}, status=status.HTTP_200_OK),
        except Exception as e:
            print("닉네임 중복 체크 중 에러 발생:", e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
