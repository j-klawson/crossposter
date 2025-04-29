#!/usr/bin/env python3

"""
crosspost.py

Cross-posting script for Mastodon and Bluesky.

This script reads configuration from a JSON file (`config.json`) and secrets from
an environment file (`config.env`) to post a single message to multiple configured
Mastodon and Bluesky accounts.

Usage:
    ./crosspost.py "Your post content here with https://links.example"

Requirements:
    - Python 3.7+
    - Mastodon.py
    - atproto
    - python-dotenv

Features:
    - Posts a single message to multiple Mastodon and Bluesky accounts.
    - Enables/disables each platform via config.
    - Supports account-specific credentials via environment variables.
    - CLI interface for entering post content.

Files:
    - config.env: Contains secrets (tokens and app passwords).
    - config.json: Contains account and platform configuration.
    - config.example.json: Shareable version of config.json without secrets.

Author:
    Your Name or GitHub handle

License:
    MIT or your preferred license
"""

import os
import json
import argparse
import re
from mastodon import Mastodon
from atproto import Client, models
from dotenv import load_dotenv, find_dotenv
from datetime import datetime, timezone

# Load .env
dotenv_path = find_dotenv("config.env")
if not dotenv_path or not load_dotenv(dotenv_path):
    print("❌ Error: Could not find or load 'config.env'.")
    sys.exit(1)

# Load config.json
try:
    with open("config.json") as f:
        config = json.load(f)
except FileNotFoundError:
    print("❌ Error: 'config.json' not found.")
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"❌ Error parsing 'config.json': {e}")
    sys.exit(1)

# === PARSE CLI ===
parser = argparse.ArgumentParser(description="Crosspost to Mastodon and Bluesky.")
parser.add_argument("text", type=str, help="The post text (surround in quotes if it contains spaces or URLs).")
args = parser.parse_args()

POST_TEXT = args.text

# === POST TO MASTODON ACCOUNTS ===
def post_to_mastodon(text):
    accounts = config["mastodon"].get("accounts", [])
    for account in accounts:
        token = os.getenv(account["token_env"])
        if not token:
            print(f"⚠️ Missing token for Mastodon account '{account['name']}'")
            continue
        try:
            mastodon = Mastodon(access_token=token, api_base_url=account["instance"])
            mastodon.status_post(text)
            print(f"✅ Posted to Mastodon ({account['name']})")
        except Exception as e:
            print(f"❌ Error posting to Mastodon ({account['name']}): {e}")

# === POST TO BLUESKY ACCOUNTS ===
def post_to_bluesky(text):
    accounts = config["bluesky"].get("accounts", [])
    for account in accounts:
        password = os.getenv(account["password_env"])
        if not password:
            print(f"⚠️ Missing password for Bluesky account '{account['name']}'")
            continue
        try:
            client = Client()
            client.login(account["handle"], password)

            # Find all URLs in the text
            urls = re.findall(r'(https?://\S+)', text)
            facets = []
            for url in urls:
                start = text.index(url)
                end = start + len(url)
                facet = models.AppBskyRichtextFacet.Main(
                    features=[models.AppBskyRichtextFacet.Link(uri=url)],
                    index=models.AppBskyRichtextFacet.ByteSlice(
                        byteStart=start,
                        byteEnd=end
                    )
                )
                facets.append(facet)

            client.send_post(text, facets=facets)

            print(f"✅ Posted to Bluesky ({account['name']})")
        except Exception as e:
            print(f"❌ Error posting to Bluesky ({account['name']}): {e}")

# === MAIN ===
if __name__ == "__main__":
    if config.get("mastodon", {}).get("enabled", False):
        post_to_mastodon(POST_TEXT)
    if config.get("bluesky", {}).get("enabled", False):
        post_to_bluesky(POST_TEXT)

