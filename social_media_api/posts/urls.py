from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedViewSet
from django.urls import path, include

router = DefaultRouter()
router.register('posts', PostViewSet, basename='post')
router.register('comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', FeedViewSet.as_view(), name='feed'),
    path('<int:pk>/like/', PostViewSet.as_view({'post': 'like'}), name='post-like'),
    path('<int:pk>/unlike/', PostViewSet.as_view({'post': 'unlike'}), name='post-unlike'),
]
