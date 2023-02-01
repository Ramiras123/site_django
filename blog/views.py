from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin


class UserPostListView(ListView):
    """Вывод ленты определенного пользователя"""
    model = Post
    template_name = 'blog/user_posts.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context['author_posts'] = get_object_or_404(User, username=self.kwargs.get('username'))
        context['posts_list'] = Post.objects.filter(author=user).order_by('-date_created')
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """Создание новой записии через форму"""
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDetailView(DetailView):
    """Страница  детали записи"""
    model = Post
    context_object_name = 'post_detail'
