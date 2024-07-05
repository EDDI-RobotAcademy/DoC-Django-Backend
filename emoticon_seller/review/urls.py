from django.urls import path, include
from rest_framework.routers import DefaultRouter

from review.controller.views import ReviewView

router = DefaultRouter()
router.register(r'review', ReviewView)

urlpatterns = [
    path('', include(router.urls)),
    path('list/', ReviewView.as_view({'get': 'list'}), name='review-list'),
    path('register/<int:pk>', ReviewView.as_view({'post': 'register'}), name='review-register'),
    path('read/<int:pk>', ReviewView.as_view({'get': 'read'}), name='review-read'),
    path('modify/<int:pk>', ReviewView.as_view({'put': 'modifyReview'}), name='review-modify'),
    path('delete/<int:pk>', ReviewView.as_view({'delete': 'removeReview'}), name='review-remove'),
    path('product/list/<int:pk>', ReviewView.as_view({'get': 'productReviewList'}), name='review-product-list'),
]

