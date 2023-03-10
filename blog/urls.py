from django.urls import path
from blog.views import UserPostListView, PostCreateView, PostDetailView, PostDeleteView, PostUpdateView
from . import views

app_name = 'blog'
urlpatterns = [
    path('posts/user/<str:username>/', UserPostListView.as_view(), name='user-posts-list'),
    path('post/new/', PostCreateView.as_view(), name='post-creat-view'),
    path('post/<int:pk>/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('', views.index, name='home'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update')
]
