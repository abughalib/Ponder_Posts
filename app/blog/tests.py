from django.test import RequestFactory, TestCase, Client
from django.contrib.auth.models import AnonymousUser, User

from blog.views import *
from blog.models import Post
from datetime import datetime
from django.urls import reverse, resolve
import pytz

# Create your tests here.


class PageTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='tester',
            email='test_user@example.com',
            password='top_secret_password'
        )

    def test_post_view_page(self):
        """ Test Home Page is Visible to All """

        request = self.factory.get('/')
        request.user = AnonymousUser()
        response = PostListView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_create_post_page_non_auth(self):
        """ Test Create Post Page for non authentication user """

        request = self.factory.get('/post/new')
        request.user = AnonymousUser()
        response = PostCreateView.as_view()(request)

        self.assertEqual(response.status_code, 302)

    def test_create_post_page_auth_user(self):
        """ Test Create Post for Authenticated User """

        request = self.factory.get('/post/new')
        request.user = self.user
        response = PostCreateView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_create_post_non_auth_user(self):
        """ Test Create Post for non Authenticated User """

        payload = {
            'title': 'abc',
            'content': 'example content'
        }

        request = self.factory.post('/post/new', payload)
        request.user = AnonymousUser()
        response = PostCreateView.as_view()(request)

        self.assertEqual(response.status_code, 302)

    def test_create_post_auth_user(self):
        """ Test Create Post for Authencticated User """

        payload = {
            'title': 'abc',
            'content': 'example content'
        }

        request = self.factory.post('/post/new', payload)
        request.user = self.user
        response = PostCreateView.as_view()(request)

        self.assertEqual(response.status_code, 302)


class TestPostUpdateView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='tester',
            email='test_user@example.com',
            password='top_secret_password'
        )
        self.post = Post.objects.create(
            title='title',
            content='example content',
            date_posted=datetime.now(tz=pytz.UTC),
            author=self.user
        )

    def test_post_update_url(self):
        """ Test Update View URL """
        url = reverse('post-update', args=[self.post.pk])
        self.assertEquals(resolve(url).func.view_class, PostUpdateView)

    def test_post_update_page_no_auth(self):
        """ Test Update Page No auth """
        url = reverse('post-update', kwargs={'pk': self.post.pk})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

    def test_post_update_page_auth(self):
        """ Test Update Page For Auth """

        url = reverse('post-update', args=(self.post.pk, ))
        self.client.login(username=self.user.username,
                          password='top_secret_password')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
