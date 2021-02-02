from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from posts.models import Post, Group


class NewPostFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.group = Group.objects.create(
            title='Vsem privet',
            slug='test-slug',
            description='Gruppa chtoby govorit privet',
        )

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='Mike')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_new_post_page_create(self):
        posts_count = Post.objects.count()
        form_data = {'group': NewPostFormTest.group.id,
                     'text': 'Текст'}
        response = self.authorized_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, '/')
        self.assertEqual(Post.objects.count(), posts_count + 1)
