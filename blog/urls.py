from django.urls import path
from blog.views import UserPostListView, PostCreateView, PostDetailView, PostDeleteView, PostUpdateView, HomePostListViewAllUsers
from . import views

app_name = 'blog'
urlpatterns = [
    path('posts/user/<str:username>/', UserPostListView.as_view(), name='user-posts-list'),
    path('post/new/', PostCreateView.as_view(), name='post-creat-view'),
 #   path('post/<int:pk>/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/<slug:slug>/', PostDetailView, name='post-detail'),
    path('', views.index, name='home'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('home/', HomePostListViewAllUsers.as_view(), name='home-post-users'),
    path('saved-posts/', views.all_save_view_posts, name='all-saved'),
    path('post/save/', views.save_post_is_ajax, name='post-save'),
    path('post/liked/', views.like_post, name='like-post')
]
