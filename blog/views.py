from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from blog.models import Post
from django.contrib.auth.models import User


class UserPostListView(ListView):
    model = Post
    context_object_name = 'post_list'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_created')
