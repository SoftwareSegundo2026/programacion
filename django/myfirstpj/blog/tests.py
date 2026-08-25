from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Post


class BlogHappyPathTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
        )

    def test_get_posts_shows_created_post(self):
        post = Post.objects.create(title='Primer post', content='Contenido de prueba')

        response = self.client.get(reverse('getPosts'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.title)
        self.assertContains(response, post.content)

    def test_create_post_saves_post_and_redirects(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('createPost'),
            {'title': 'Nuevo post', 'content': 'Texto del nuevo post'},
        )

        self.assertRedirects(response, reverse('getPosts'))
        self.assertTrue(
            Post.objects.filter(
                title='Nuevo post',
                content='Texto del nuevo post',
                deleted_at__isnull=True,
            ).exists()
        )

    def test_delete_post_soft_deletes_and_hides_from_list(self):
        self.client.login(username='testuser', password='testpass123')
        post = Post.objects.create(title='Post a eliminar', content='Contenido eliminado')

        response = self.client.post(reverse('deletePost', args=[post.id]))

        self.assertRedirects(response, reverse('getPosts'))
        post.refresh_from_db()
        self.assertIsNotNone(post.deleted_at)

        response = self.client.get(reverse('getPosts'))
        self.assertNotContains(response, post.title)

    def test_deleted_posts_page_shows_deleted_post(self):
        post = Post.objects.create(title='Post eliminado', content='Contenido perdido')
        post.deleted_at = timezone.now()
        post.save()

        response = self.client.get(reverse('deletedPosts'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.title)
        self.assertContains(response, post.content)

    def test_restore_post_clears_deleted_at(self):
        self.client.login(username='testuser', password='testpass123')
        post = Post.objects.create(title='Post restaurable', content='Contenido restaurable')
        post.deleted_at = timezone.now()
        post.save()

        response = self.client.post(reverse('restorePost', args=[post.id]))

        self.assertRedirects(response, reverse('deletedPosts'))
        post.refresh_from_db()
        self.assertIsNone(post.deleted_at)
