#!/usr/bin/env python3

import os
import json
import argparse
from mastodon import Mastodon
from atproto import Client, models
from dotenv import load_dotenv

# === LOAD CONFIG ===
load_dotenv("config.env")

with open("config.json") as f:
    config = json.load(f)

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
            client.send_post(models.AppBskyFeedPost.Main(
                text=text,
                created_at=models.get_iso_timestamp(),
            ))
            print(f"✅ Posted to Bluesky ({account['name']})")
        except Exception as e:
            print(f"❌ Error posting to Bluesky ({account['name']}): {e}")

# === MAIN ===
if __name__ == "__main__":
    if config.get("mastodon", {}).get("enabled", False):
        post_to_mastodon(POST_TEXT)
    if config.get("bluesky", {}).get("enabled", False):
        post_to_bluesky(POST_TEXT)

