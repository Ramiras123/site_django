from random import random

from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from blog.models import Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from . forms import CommentForm

def index(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/index.html', context)


class UserPostListView(ListView):
    """Вывод ленты определенного пользователя"""
    model = Post
    paginate_by = 3
    template_name = 'blog/user_posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context['author_posts'] = user
        context['posts_list'] = Post.objects.filter(author=user).order_by('-date_created')
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """Создание новой записии через форму"""
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

"""
class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post_detail'
"""


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

    def get_success_url(self):
        return reverse_lazy('blog:user-posts-list', kwargs={'username': self.request.user})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/update_post.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False
        
    def get_success_url(self):
        return reverse_lazy('blog:user-posts-list', kwargs={'username': self.request.user})


def PostDetailView(request, pk, slug):
    handler_page = get_object_or_404(Post, pk=pk, slug=slug)
    total_comments = handler_page.comments_blog.all().filter(replay_comment=None).order_by('-pk')
    total_comments_2 = handler_page.comments_blog.all().order_by('-pk')
    total_likes = handler_page.total_likes_post()
    total_saves = handler_page.total_saves_posts()
    context = {}
    if request.method == "POST":
        comments_qs = None
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            form = request.POST.get('body')
            comment = Comment.objects.create(name_author=request.user,
                                             body=form,
                                             post=handler_page,
                                             replay_comment=comments_qs)
            comment.save()
            total_comments = handler_page.comments_blog.all().filter(replay_comment=None).order_by('-pk')
    else:
        comment_form = CommentForm()
    saved = False
    if handler_page.saves_posts.filter(id=request.user.id).exists():
        saved = True
    liked = False
    if handler_page.likes_post.filter(id=request.user.id).exists():
        liked = True
    context['total_saves'] = total_saves
    context['saved'] = saved
    context['liked'] = liked
    context['total_likes'] = total_likes
    context['comment_form'] = comment_form
    context['comments'] = total_comments
    context['post_detail'] = handler_page
    if request.is_ajax():
        html = render_to_string('blog/comments.html', context)
        return JsonResponse({"form": html})
    return render(request, 'blog/post_detail.html', context)


class HomePostListViewAllUsers(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = "posts"
    ordering = ['-date_created']
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomePostListViewAllUsers, self).get_context_data()
        users = list(User.objects.exclude(pk=self.request.user.pk))
        if len(users) > 3:
            out = 3
        else:
            out = len(users)
        random_users = random.sample(users, out)
        context['random_users'] = random_users
        return context


def all_save_view_posts(request):
    user = request.user
    saved_posts = user.blog_posts_save.all()
    context = {'saved_posts': saved_posts}
    return render(request, 'blog/saved_posts.html', context)


@login_required
def save_post_is_ajax(request):
    post = get_object_or_404(Post, id=request.POST.get('id'))
    saved = False
    if post.saves_posts.filter(id=request.user.id).exists():
        post.saves_posts.remove(request.user)
        saved = False
    else:
        post.saves_posts.add(request.user)
        saved = True
    context = {
        'post_detail': post,
        'total_saves': post.total_saves_posts(),
        'saved': saved
    }
    if request.is_ajax():
        html = render_to_string('blog/save_section.html', context, request=request)
        return JsonResponse({'form': html})


@login_required
def like_post(request):
    post = get_object_or_404(Post, id=request.POST.get('id'))
    like = False
    if post.likes_post.filter(id=request.user.id).exists():
        post.likes_post.remove(request.user)
        like = False
    else:
        post.likes_post.add(request.user)
        like = True
    context = {
        'post_detail': post,
        'total_likes': post.total_likes_post(),
        'liked': like,
    }
    if request.is_ajax():
        html = render_to_string('blog/likes_section.html', context, request=request)
        return  JsonResponse({'form':html})