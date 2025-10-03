from django.contrib import admin
from django.urls import path
from .views import RegisterView, CustomLoginView, CustomLogoutView, ProfileView
from .views import (PostListView, PostDetailView,PostCreateView, PostUpdateView, PostDeleteView)

app_name = 'blog'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('', PostListView.as_view(), name='post-list'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
]
