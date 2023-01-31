from django.test import TestCase, Client
from blog.models import Post
from django.contrib.auth.models import User


class PostPageUrls(TestCase):

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        Post.objects.create(
            title='Тестовый заголовок',
            author=self.user,
            slug='test-slug'
        )

    def test_about_url_exists_at_desired_location(self):
        """Проверка доступности адреса posts/user/<str:username>/"""
        response = self.guest_client.get('/posts/user/HasNoName/')
        self.assertEqual(response.status_code, 200)

    def test_about_url_uses_correct_template(self):
        """Проверка шаблона для адреса posts/user/<str:username>/"""
        templates_url_names = {
            'blog/user_posts.html': '/posts/user/HasNoName/',
        }
        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
