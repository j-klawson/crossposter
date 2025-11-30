"""Command-line interface for crosspost."""

import argparse
from .config import load_config
from .poster import post_to_mastodon, post_to_bluesky


def main():
    """Main entry point for the crosspost CLI."""
    parser = argparse.ArgumentParser(
        description="Post to Mastodon and Bluesky simultaneously."
    )
    parser.add_argument(
        "text",
        type=str,
        help="The post text (surround in quotes if it contains spaces or URLs)."
    )
    args = parser.parse_args()

    # Load configuration
    config = load_config()

    # Post to enabled platforms
    post_to_mastodon(args.text, config)
    post_to_bluesky(args.text, config)


if __name__ == "__main__":
    main()
