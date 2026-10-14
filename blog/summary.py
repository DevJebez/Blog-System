"""Extractive post summaries: the sentences closest to the post's overall meaning (TextRank-style)."""
import logging
import re

import numpy as np

from .models import Post
from .semantic import _encode

logger = logging.getLogger(__name__)

MIN_WORDS = 60  # shorter posts are already their own summary
SENTENCES = 2


def split_sentences(text):
    parts = re.split(r'(?<=[.!?])\s+|\n+', text.strip())
    return [p.strip() for p in parts if len(p.split()) >= 4]


def summarize(text, count=SENTENCES):
    """Return the `count` most central sentences in their original order ('' if the text is short)."""
    if len(text.split()) < MIN_WORDS:
        return ''
    sentences = split_sentences(text)
    if len(sentences) <= count:
        return ''
    vectors = _encode(sentences)  # normalised, so dot products are cosine similarities
    similarity = vectors @ vectors.T
    np.fill_diagonal(similarity, 0)
    similarity = np.clip(similarity, 0, None)
    # power iteration: a sentence is important if it is similar to other important sentences
    rank = np.ones(len(sentences)) / len(sentences)
    transition = similarity / np.maximum(similarity.sum(axis=0), 1e-9)
    for _ in range(30):
        rank = 0.15 / len(sentences) + 0.85 * transition @ rank
    top = sorted(np.argsort(rank)[::-1][:count])
    return ' '.join(sentences[i] for i in top)


def summarize_post(post):
    """Compute and store the summary of `post`; failures never block saving."""
    try:
        summary = summarize(post.content)
    except Exception:
        logger.exception('Could not summarize post %s', post.pk)
        return
    Post.objects.filter(pk=post.pk).update(summary=summary)
