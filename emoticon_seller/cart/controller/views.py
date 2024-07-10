from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from account.service.account_service_impl import AccountServiceImpl
from cart.entity.cart_item import CartItem
from cart.repository.cart_item_repository_impl import CartItemRepositoryImpl
from cart.repository.cart_repository_impl import CartRepositoryImpl
from cart.service.cart_service_impl import CartServiceImpl
from oauth.service.redis_service_impl import RedisServiceImpl


class CartView(viewsets.ViewSet):
    cartService = CartServiceImpl.getInstance()
    cartRepository = CartRepositoryImpl.getInstance()
    cartItemRepository = CartItemRepositoryImpl.getInstance()
    redisService = RedisServiceImpl.getInstance()
    accountService = AccountServiceImpl.getInstance()

    def cartItemList(self, request):
        data = request.data
        userToken = data.get('userToken')

        if not userToken:
            return Response({'error': 'User token is required'}, status=status.HTTP_400_BAD_REQUEST)

        accountId = self.redisService.getValueByKey(userToken)
        if not accountId:
            return Response({'error': 'Invalid user token'}, status=status.HTTP_400_BAD_REQUEST)

        cartItemListResponseForm = self.cartService.cartList(accountId)
        return Response(cartItemListResponseForm, status=status.HTTP_200_OK)

    def cartRegister(self, request):
        try:
            data = request.data
            print('data:', data)

            userToken = data.get('userToken')
            accountId = self.redisService.getValueByKey(userToken)

            self.cartService.cartRegister(data, accountId)
            return Response(status=status.HTTP_200_OK)

        except Exception as e:
            print('상품 등록 과정 중 문제 발생:', e)
            return Response({ 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def removeCartItem(self, request):
        data = request.data

        if list(data.keys())[0] == 'productId':
            cartItemList = CartItem.objects.all()
            for cartItem in cartItemList:
                if cartItem.product.productId == data['productId'][0]:
                    self.cartService.removeCartItem([cartItem.cartItemId])

        if list(data.keys())[0] == 'CartItemId':
            self.cartService.removeCartItem(data['CartItemId'])

        return Response(status=status.HTTP_204_NO_CONTENT)

    def checkCartItemDuplication(self, request):
        userToken = request.data['payload']['userToken']
        productId = request.data['payload']['productId']

        accountId = self.redisService.getValueByKey(userToken)
        account = self.accountService.findAccountById(accountId)
        cart = self.cartRepository.findByAccount(account)
        cartItemList = self.cartItemRepository.findByCart(cart)
        isDuplicate = self.cartItemRepository.checkDuplication(cartItemList, productId)
        print(f"isDuplicate: {isDuplicate}")
        return Response(isDuplicate, status=status.HTTP_200_OK)

