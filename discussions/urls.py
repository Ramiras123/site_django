from django.urls import path
from discussions.views import UserDiscussionsListView, DiscussionsDetailView, discussion_create
app_name = 'discussion'
urlpatterns = [
    path('discussion/<str:username>/', UserDiscussionsListView.as_view(), name='user-discussion-list'),
    path('discussion/<int:pk>/<slug:slug>/', DiscussionsDetailView.as_view(), name='discussion-detail'),
    path('create/', discussion_create, name='create'),
]