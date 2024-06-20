from django.urls import path, include
from rest_framework.routers import DefaultRouter

from board.controller.views import BoardView

router = DefaultRouter()
router.register(r'board', BoardView)

urlpatterns = [
    path('', include(router.urls)),
    path('list/', BoardView.as_view({'get': 'list'}), name='board-list'),
    path('register', BoardView.as_view({'post': 'register'}), name='board-register'),
    path('read/<int:pk>', BoardView.as_view({'get': 'read'}), name='board-read'),
    path('modify/<int:pk>', BoardView.as_view({'put': 'modifyBoard'}), name='board-modify'),
    path('delete/<int:pk>', BoardView.as_view({'delete': 'removeBoard'}), name='board-remove'),
]

