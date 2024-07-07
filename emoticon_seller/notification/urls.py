from django.urls import path, include
from rest_framework.routers import DefaultRouter

from notification.controller.views import NotificationView

router = DefaultRouter()
router.register(r'notification', NotificationView, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
    path('list/', NotificationView.as_view({'post': 'expectedSecedeAccount'}), name='notification-list'),
]
