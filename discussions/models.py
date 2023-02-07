from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from ckeditor.fields import RichTextField
from pytils.translit import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Discussions(models.Model):
    """Модель для создания постов"""
    class Meta:
        verbose_name = 'Дискуссия'
        verbose_name_plural = 'Дискуссия'

    title = models.CharField(max_length=200, db_index=True)
    content = RichTextField(max_length=2000, blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField()
    likes_discussion = models.ManyToManyField(User, related_name='discussion_likes', blank=True,
                                              verbose_name='Лайки')
    saves_discussion = models.ManyToManyField(User, related_name="blog_discussion_save", blank=True,
                                              verbose_name='Сохранённые посты пользователя')

    def total_likes_discussions(self):
        return self.likes_discussion.count()

    def total_saves_discussions(self):
        return self.saves_discussion.count()

    def get_absolute_url(self):
        return reverse('discussion:discussion-detail', kwargs={'slug': self.slug, 'pk': self.pk})

    def __str__(self):
        return self.title


@receiver(pre_save, sender=Discussions)
def prepopulated_slug(sender, instance, **kwargs):
    instance.slug = slugify(instance.title)
