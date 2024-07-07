from django.http import JsonResponse
from rest_framework import viewsets, status
from datetime import datetime

from account.repository.profile_repository_impl import ProfileRepositoryImpl
from orders.service.orders_service_impl import OrdersServiceImpl

class NotificationView(viewsets.ViewSet):
    ordersService = OrdersServiceImpl.getInstance()
    profileRepository = ProfileRepositoryImpl.getInstance()


    def expectedSecedeAccount(self, request):
        ordersList = self.ordersService.getAllOrders()
        accountIdList = []

        for orders in ordersList:
            if orders.account_id not in accountIdList:
                accountIdList.append(orders.account_id)

        currentTime = datetime.now().timestamp()
        standardDate = 5184000
        serializedAccountList = []

        for accountId in accountIdList:
            ordersListByAccountId = self.ordersService.findAllByAccountId(accountId)
            if len(ordersListByAccountId) > 1:
                createdDateList = list(ordersListByAccountId.values_list('createdDate', flat=True))
                lastOrderedDate = max(createdDateList)
            else:
                lastOrderedDate = list(ordersListByAccountId.values_list('createdDate', flat=True))[0]

            lastOrderedDate = datetime.strptime(lastOrderedDate, "%Y-%m-%d %H:%M:%S")

            if currentTime - lastOrderedDate.timestamp() > standardDate:
                serializedAccountList.append({
                    'accountId': accountId,
                    'email': self.profileRepository.findById(accountId).email,
                    'lastOrderedDate': lastOrderedDate.strftime("%Y-%m-%d %H:%M:%S")
                })

        return JsonResponse(serializedAccountList, safe=False, status=status.HTTP_200_OK)
