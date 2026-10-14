from django.db.models.signals import post_save
from django.dispatch import receiver

from .ml import extract_keywords
from .semantic import embed_post
from .summary import summarize_post
from .models import Post, Tag


@receiver(post_save, sender=Post)
def tag_post(sender, instance, **kwargs):
    """Regenerate a post's tags from its text every time it is saved."""
    tags = [Tag.objects.get_or_create(name=word)[0] for word in extract_keywords(instance)]
    instance.tags.set(tags)


@receiver(post_save, sender=Post)
def embed_saved_post(sender, instance, **kwargs):
    """Store a sentence embedding for semantic search."""
    embed_post(instance)


@receiver(post_save, sender=Post)
def summarize_saved_post(sender, instance, **kwargs):
    """Store a short summary for long posts."""
    summarize_post(instance)
