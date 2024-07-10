from django.urls import path, include
from rest_framework.routers import DefaultRouter

from account.controller.views import AccountView

router = DefaultRouter()
router.register(r'account', AccountView, basename='account')

urlpatterns = [
    path('', include(router.urls)),
    path('email-duplication-check',
         AccountView.as_view({'post': 'checkEmailDuplication'}),
         name='account-email-duplication-check'),
    path('nickname-duplication-check',
         AccountView.as_view({'post': 'checkNicknameDuplication'}),
         name='account-nickname-duplication-check'),
    path('register',
         AccountView.as_view({'post': 'registerAccount'}),
         name='account-register'),
    path('nickname',
         AccountView.as_view({'post': 'getNickname'}),
         name='account-nickname'),
    path('roleType',
         AccountView.as_view({'post': 'getRoleType'}),
         name='account-roleType'),
    path('admin/password',
         AccountView.as_view({'post': 'getAdminPassword'}),
         name='account-admin-password'),
    path('recommend/register',
         AccountView.as_view({'post': 'registerRecommend'}),
         name='account-recommend-register'),
    path('recommend/list',
         AccountView.as_view({'post': 'recommendProductIdList'}),
         name='account-recommend-list'),
]