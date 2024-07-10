from django.urls import path, include
from rest_framework.routers import DefaultRouter

from orders.controller.views import OrdersView

router = DefaultRouter()
router.register(r'orders', OrdersView, basename='orders')

urlpatterns = [
    path('', include(router.urls)),
    path('cart', OrdersView.as_view({'post': 'createCartOrders'}), name='order-cart'),
    path('product', OrdersView.as_view({'post': 'createProductOrders'}), name='order-product'),
    path('notification', OrdersView.as_view({'post': 'findAccountToNotification'}), name='order-notification'),
    path('list/', OrdersView.as_view({'post': 'myOrderList'}), name='order-list'),
    path('read/<int:pk>', OrdersView.as_view({'post': 'myOrderItemList'}), name='order-item-list'),
    path('order-item-duplication-check', OrdersView.as_view({'post': 'checkOrderItemDuplication'}),
         name='order-item-duplication-check'),
]
