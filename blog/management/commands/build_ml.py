from django.core.management.base import BaseCommand

from blog.models import Post
from blog.signals import embed_saved_post, summarize_saved_post, tag_post


class Command(BaseCommand):
    help = 'Generate tags, summaries and search embeddings for all existing posts.'

    def handle(self, *args, **options):
        posts = Post.objects.all()
        for post in posts:
            tag_post(Post, post)
            embed_saved_post(Post, post)
            summarize_saved_post(Post, post)
        self.stdout.write(self.style.SUCCESS(f'Processed {posts.count()} posts.'))
