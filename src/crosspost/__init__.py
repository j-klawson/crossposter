"""Crosspost: Post to Mastodon & Bluesky simultaneously."""

__version__ = "0.1.0"

from .config import load_config
from .poster import post_to_mastodon, post_to_bluesky

__all__ = [
    "load_config",
    "post_to_mastodon",
    "post_to_bluesky",
]
