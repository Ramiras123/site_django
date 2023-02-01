from django.urls import path
from blog.views import UserPostListView, PostCreateView, PostDetailView
app_name = 'blog'
urlpatterns = [
    path('posts/user/<str:username>/', UserPostListView.as_view(), name='user-posts-list'),
    path('post/new/', PostCreateView.as_view(), name='post-creat-view'),
    path('post/<int:pk>/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
]
