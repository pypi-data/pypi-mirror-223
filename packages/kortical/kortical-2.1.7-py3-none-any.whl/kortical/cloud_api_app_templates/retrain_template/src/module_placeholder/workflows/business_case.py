import logging

logger = logging.getLogger(__name__)


def should_publish(challenger_score, champion_score):
    # Add extra requirements here.
    return challenger_score > champion_score
