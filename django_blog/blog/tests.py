from django.test import TestCase
from .models import Post, Tag
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class TaggingSearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u', password='p')
        self.post1 = Post.objects.create(title='Django tips', content='Learn Django', author=self.user)
        self.post2 = Post.objects.create(title='Python tips', content='Learn Python', author=self.user)
        t1 = Tag.objects.create(name='django')
        self.post1.tags.add(t1)
        t2 = Tag.objects.create(name='python')
        self.post2.tags.add(t2)

    def test_posts_by_tag(self):
        resp = self.client.get(reverse('posts-by-tag', kwargs={'tag_slug': 'django'}))
        self.assertContains(resp, 'Django tips')
        self.assertNotContains(resp, 'Python tips')

    def test_search_by_keyword(self):
        resp = self.client.get(reverse('search-results') + '?q=Python')
        self.assertContains(resp, 'Python tips')
