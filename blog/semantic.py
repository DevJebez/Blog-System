"""Semantic search: posts are embedded with a sentence-transformers model and ranked by cosine similarity."""
import logging
from functools import lru_cache

import numpy as np

from .models import Post

logger = logging.getLogger(__name__)

MODEL_NAME = 'all-MiniLM-L6-v2'
MIN_SCORE = 0.25


@lru_cache(maxsize=1)
def _model():
    # loaded once per process on first use (downloads ~90 MB the first time)
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(MODEL_NAME)


def _encode(text):
    return _model().encode(text, normalize_embeddings=True)


def embed_post(post):
    """Compute and store the embedding of `post`; failures never block saving a post."""
    try:
        vector = _encode(f"{post.title}. {post.content}")
    except Exception:
        logger.exception('Could not embed post %s', post.pk)
        return
    Post.objects.filter(pk=post.pk).update(embedding=[float(x) for x in vector])


def semantic_search(query, limit=10):
    """Return `[(post, score)]` best matches for `query`; falls back to substring search if the model is unavailable."""
    try:
        query_vector = _encode(query)
    except Exception:
        logger.exception('Semantic search unavailable, using keyword fallback')
        return [(p, None) for p in Post.objects.filter(title__icontains=query).select_related('author')[:limit]]
    posts = list(Post.objects.exclude(embedding__isnull=True).select_related('author'))
    if not posts:
        return []
    matrix = np.array([p.embedding for p in posts])
    scores = matrix @ query_vector
    ranked = sorted(zip(scores, posts), key=lambda pair: pair[0], reverse=True)
    return [(p, float(s)) for s, p in ranked[:limit] if s >= MIN_SCORE]
