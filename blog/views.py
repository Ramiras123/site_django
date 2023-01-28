from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from blog.models import Post
from django.contrib.auth.models import User


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context['author_posts'] = get_object_or_404(User, username=self.kwargs.get('username'))
        context['posts_list'] = Post.objects.filter(author=user).order_by('-date_created')
        return context
