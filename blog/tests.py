from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .ml import related_posts
from .models import Post


class MLFeatureTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user('alice', password='pw')
        cls.py1 = Post.objects.create(author=user, title='Django models',
                                      content='Django models map python classes to database tables and queries.')
        cls.py2 = Post.objects.create(author=user, title='Django queries',
                                      content='Django queries use the python ORM to read database tables.')
        cls.cook = Post.objects.create(author=user, title='Pasta recipe',
                                       content='Boil pasta, add tomato sauce and basil for dinner.')

    def test_related_posts_prefers_similar_topic(self):
        related = related_posts(self.py1)
        self.assertEqual(related[0], self.py2)
        self.assertNotIn(self.cook, related)

    def test_tags_generated_on_save(self):
        self.assertTrue(self.py1.tags.filter(name='django').exists())

    def test_pages_render(self):
        self.assertContains(self.client.get(reverse('post-detail', args=[self.py1.pk])), 'You might also like')
        self.assertEqual(self.client.get(reverse('tag-posts', args=['django'])).status_code, 200)
        self.assertEqual(self.client.get(reverse('blog-home')).status_code, 200)
        self.assertEqual(self.client.get(reverse('user-posts', args=['alice'])).status_code, 200)


class SemanticSearchTests(TestCase):
    def test_search_finds_post_without_shared_words(self):
        user = User.objects.create_user('bob', password='pw')
        Post.objects.create(author=user, title='Cooking pasta', content='Boil noodles and add tomato sauce for dinner.')
        Post.objects.create(author=user, title='Learning Python', content='Variables, loops and functions for beginners.')
        response = self.client.get(reverse('blog-search'), {'q': 'how to make an Italian meal'})
        results = response.context['results']
        self.assertEqual(results[0][0].title, 'Cooking pasta')
        self.assertEqual(self.client.get(reverse('blog-search')).status_code, 200)


class CommentModerationTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user('carol', password='pw')
        self.reader = User.objects.create_user('dave', password='pw')
        self.post = Post.objects.create(author=self.author, title='Hello', content='First post body text.')

    def comment(self, text):
        self.client.login(username='dave', password='pw')
        self.client.post(reverse('comment-create', args=[self.post.pk]), {'content': text})
        return self.post.comments.get()

    def test_friendly_comment_is_approved(self):
        self.assertTrue(self.comment('Great post, thanks for sharing!').is_approved)

    def test_toxic_comment_is_held_and_hidden_from_others(self):
        c = self.comment('You are an idiot and I hate you')
        self.assertFalse(c.is_approved)
        self.assertGreater(c.toxicity, 0.7)
        self.client.logout()
        self.assertNotContains(self.client.get(self.post.get_absolute_url()), 'idiot')
        self.client.login(username='dave', password='pw')
        self.assertContains(self.client.get(self.post.get_absolute_url()), 'Held for review')

    def test_post_owner_can_delete_comment(self):
        c = self.comment('Nice one')
        self.client.login(username='carol', password='pw')
        self.assertEqual(self.client.post(reverse('comment-delete', args=[c.pk])).status_code, 302)
        self.assertFalse(self.post.comments.exists())

    def test_anonymous_cannot_comment(self):
        self.client.logout()
        self.client.post(reverse('comment-create', args=[self.post.pk]), {'content': 'hi'})
        self.assertFalse(self.post.comments.exists())


class SummaryTests(TestCase):
    LONG = (
        "Django is a high level Python web framework that encourages rapid development. "
        "It follows the model template view pattern and ships with an object relational mapper. "
        "Developers define models as Python classes and Django creates the database tables for them. "
        "The built in admin interface lets you manage the stored data without writing extra code. "
        "My cat likes to sleep on the keyboard while I write code in the afternoon. "
        "Django also includes authentication, forms, sessions and security protections by default. "
        "Because so many features are included, teams can build complete websites very quickly."
    )

    def test_long_post_gets_short_summary(self):
        user = User.objects.create_user('erin', password='pw')
        post = Post.objects.create(author=user, title='About Django', content=self.LONG)
        post.refresh_from_db()
        self.assertTrue(post.summary)
        self.assertLess(len(post.summary), len(self.LONG))
        self.assertTrue(all(s in self.LONG for s in post.summary.split('. ')[:1]))
        self.assertContains(self.client.get(post.get_absolute_url()), 'TL;DR')

    def test_short_post_has_no_summary(self):
        user = User.objects.create_user('frank', password='pw')
        post = Post.objects.create(author=user, title='Hi', content='Just a short post here.')
        post.refresh_from_db()
        self.assertEqual(post.summary, '')
