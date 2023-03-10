from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from ckeditor.fields import RichTextField
from pytils.translit import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Post(models.Model):
    """Модель для создания постов"""
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    title = models.CharField(max_length=200, db_index=True)
    content = RichTextField(max_length=2000, blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField()
    likes_post = models.ManyToManyField(User, related_name='post_likes', blank=True,
                                        verbose_name='Лайки')
    saves_posts = models.ManyToManyField(User, related_name="blog_posts_save", blank=True,
                                         verbose_name='Сохранённые посты пользователя')

    def total_likes_post(self):
        return self.likes_post.count()

    def total_saves_posts(self):
        return self.saves_posts.count()

    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={'slug': self.slug, 'pk': self.pk})

    def __str__(self):
        return self.title


@receiver(pre_save, sender=Post)
def prepopulated_slug(sender, instance, **kwargs):
    instance.slug = slugify(instance.title)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments_blog', on_delete=models.CASCADE)
    name_author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    likes_comment = models.ManyToManyField(User, related_name='likes_blog_comments', blank=True)
    replay_comment = models.ForeignKey('self', null=True, related_name='replies_comment', on_delete=models.CASCADE)

    def total_likes(self):
        return self.likes_comment.count()

    def __str__(self):
        return f"{self.post.title} {self.name_author} {self.id}"

    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={'pk': self.pk})
