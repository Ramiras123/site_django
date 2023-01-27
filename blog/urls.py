from django.urls import path
from blog.views import UserPostListView
app_name = 'blog'
urlpatterns = [
    path('posts/user/<str:username>/', UserPostListView.as_view(), name='user-posts-list'),
]