"""Comment moderation with the unitary/toxic-bert multi-label toxicity classifier."""
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)

MODEL_NAME = 'unitary/toxic-bert'
THRESHOLD = 0.7  # comments scoring at or above this are held for review


@lru_cache(maxsize=1)
def _classifier():
    from transformers import pipeline
    return pipeline('text-classification', model=MODEL_NAME, top_k=None, function_to_apply='sigmoid')


def toxicity_score(text):
    """Highest toxicity label probability (0-1), or None if the model is unavailable."""
    try:
        return max(item['score'] for item in _classifier()(text, truncation=True)[0])
    except Exception:
        logger.exception('Toxicity model unavailable')
        return None


def moderate(comment):
    """Score `comment` and set `is_approved`. If the model fails the comment is held (fail closed)."""
    comment.toxicity = toxicity_score(comment.content)
    comment.is_approved = comment.toxicity is not None and comment.toxicity < THRESHOLD
    return comment.is_approved
