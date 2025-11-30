"""Command-line interface for crosspost."""

import argparse
import sys
from .config import load_config, setup_keychain
from .poster import post_to_mastodon, post_to_bluesky, post_to_twitter


def main():
    """Main entry point for the crosspost CLI."""
    parser = argparse.ArgumentParser(
        description="Post to Mastodon, Bluesky, and Twitter simultaneously."
    )
    parser.add_argument(
        "text",
        nargs="?",
        type=str,
        help="The post text (surround in quotes if it contains spaces or URLs)."
    )
    parser.add_argument(
        "--setup",
        action="store_true",
        help="Set up Keychain credentials interactively (does not post)."
    )
    args = parser.parse_args()

    # Load configuration (skip prompts during setup)
    config = load_config(skip_prompts=args.setup)

    # Handle setup mode
    if args.setup:
        try:
            setup_keychain(config)
            sys.exit(0)
        except KeyboardInterrupt:
            print("\n⏭️  Setup cancelled")
            sys.exit(0)

    # Require text for posting
    if not args.text:
        parser.print_help()
        sys.exit(1)

    # Post to enabled platforms
    post_to_mastodon(args.text, config)
    post_to_bluesky(args.text, config)
    post_to_twitter(args.text, config)


if __name__ == "__main__":
    main()
