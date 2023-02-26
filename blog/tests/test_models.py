import pytest

from blog.models import Post
from django.test import TestCase
from django.contrib.auth.models import User


@pytest.mark.django_db
class PostTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='test', password='test123')
        Post.objects.create(title='13', author=user, content='134', slug='slug_test')

    def test_model_create(self):
        model = Post.objects.get(title='13')
        self.assertEqual(model.title, '13')
        self.assertEqual(model.content, '134')
        self.assertTrue(model.date_created)
        self.assertTrue(model.date_updated)
        self.assertEqual(model.slug, '13')
