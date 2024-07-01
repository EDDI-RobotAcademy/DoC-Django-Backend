from django.urls import path, include
from rest_framework.routers import DefaultRouter

from review.controller.views import ReviewView

router = DefaultRouter()
router.register(r'review', ReviewView)

urlpatterns = [
    path('', include(router.urls)),
    path('list/', ReviewView.as_view({'get': 'list'}), name='review-list'),
    path('register', ReviewView.as_view({'post': 'register'}), name='review-register'),
]
