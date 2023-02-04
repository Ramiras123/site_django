from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from discussions.models import Discussions
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from discussions.forms import DiscussionCreateForm
from django.shortcuts import render


class UserDiscussionsListView(ListView):
    """Вывод ленты определенного пользователя"""
    model = Discussions
    template_name = 'discussions/user_discussions.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context['author_discus'] = get_object_or_404(User, username=self.kwargs.get('username'))
        context['discus_list'] = Discussions.objects.filter(author=user).order_by('-date_created')
        return context


class DiscussionsDetailView(DetailView):
    """Страница  детали записи"""
    model = Discussions
    context_object_name = 'discus_detail'
    template_name = 'discussions/detail_discussions.html'


@login_required
def discussion_create(request):
    if request.method == 'POST':
        form = DiscussionCreateForm(request.POST, request.FILES)
        if form.is_valid():
            new_disc = form.save(commit=False)
            new_disc.author = request.user
            new_disc.save()
            return redirect(new_disc.get_absolute_url())
    else:
        form = DiscussionCreateForm()
    return render(request, 'discussions/create_form.html', {'form': form})
