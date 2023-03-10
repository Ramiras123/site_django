# deals/tests/test_views.py
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from blog.models import Post

User = get_user_model()


class TaskPagesTests(TestCase):

    def setUp(self):
        # Создаем авторизованный клиент
        self.user = User.objects.create_user(username='Alex')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        Post.objects.create(
            title='Заголовок',
            content='Текст',
            author=self.user,
        )

    # в первом элементе списка object_list содержит ожидаемые значения
    def test_task_list_page_show_correct_context(self):
        """Шаблон task_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('blog:user-posts-list',
                                                      kwargs={'username': 'Alex'}))
        # Взяли первый элемент из списка и проверили, что его содержание
        # совпадает с ожидаемым
        first_object = response.context['posts_list'][0]
        task_title_0 = first_object.title
        task_text_0 = first_object.content
        task_slug_0 = first_object.slug
        self.assertEqual(task_title_0, 'Заголовок')
        self.assertEqual(task_text_0, 'Текст')
        self.assertEqual(task_slug_0, 'zagolovok')

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            'blog/user_posts.html': (
                reverse('blog:user-posts-list',
                        kwargs={'username': 'Alex'})),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)