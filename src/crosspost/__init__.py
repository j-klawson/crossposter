"""Crosspost: Post to Mastodon, Bluesky, and Twitter simultaneously."""

__version__ = "0.1.0"

from .config import load_config
from .poster import post_to_mastodon, post_to_bluesky, post_to_twitter

__all__ = [
    "load_config",
    "post_to_mastodon",
    "post_to_bluesky",
    "post_to_twitter",
]
