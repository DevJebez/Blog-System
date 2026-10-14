"""Lightweight NLP helpers: TF-IDF based related posts and automatic keyword tags."""
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from .models import Post

TOKEN_PATTERN = r"(?u)\b[a-zA-Z][a-zA-Z]{2,}\b"


def _text(post):
    # the title is repeated so it counts for more than a single body sentence
    return f"{post.title} {post.title} {post.content}"


def _vectorizer():
    return TfidfVectorizer(stop_words='english', sublinear_tf=True, token_pattern=TOKEN_PATTERN)


def related_posts(post, limit=3):
    """Return up to `limit` other posts ordered by cosine similarity to `post`."""
    posts = list(Post.objects.select_related('author'))
    if len(posts) < 2:
        return []
    try:
        matrix = _vectorizer().fit_transform(_text(p) for p in posts)
    except ValueError:  # every document is empty after stop-word removal
        return []
    index = next((i for i, p in enumerate(posts) if p.pk == post.pk), None)
    if index is None:
        return []
    scores = linear_kernel(matrix[index], matrix).flatten()
    ranked = sorted(
        ((score, p) for score, p in zip(scores, posts) if p.pk != post.pk and score > 0.05),
        key=lambda pair: pair[0],
        reverse=True,
    )
    return [p for _, p in ranked[:limit]]


def extract_keywords(post, limit=4):
    """Return the highest scoring TF-IDF terms of `post` relative to all posts."""
    posts = list(Post.objects.exclude(pk=post.pk)) + [post]
    try:
        vectorizer = _vectorizer()
        matrix = vectorizer.fit_transform(_text(p) for p in posts)
    except ValueError:
        return []
    row = matrix[len(posts) - 1].toarray().flatten()
    terms = vectorizer.get_feature_names_out()
    best = row.argsort()[::-1][:limit]
    return [terms[i] for i in best if row[i] > 0]
