"""Posting functionality for Mastodon and Bluesky."""

import re
from mastodon import Mastodon
from atproto import Client, models


def post_to_mastodon(text, config):
    """Post a message to configured Mastodon accounts.

    Args:
        text (str): The post text
        config (dict): Configuration dictionary with mastodon account info
    """
    if not config.get("mastodon", {}).get("enabled", False):
        return

    accounts = config.get("mastodon", {}).get("accounts", [])
    for account in accounts:
        token = account.get("token")
        if not token:
            print(f"⚠️ Missing token for Mastodon account '{account['name']}'")
            continue
        try:
            mastodon = Mastodon(access_token=token, api_base_url=account["instance"])
            mastodon.status_post(text)
            print(f"✅ Posted to Mastodon ({account['name']})")
        except Exception as e:
            print(f"❌ Error posting to Mastodon ({account['name']}): {e}")


def post_to_bluesky(text, config):
    """Post a message to configured Bluesky accounts with URL formatting.

    Args:
        text (str): The post text
        config (dict): Configuration dictionary with bluesky account info
    """
    if not config.get("bluesky", {}).get("enabled", False):
        return

    accounts = config.get("bluesky", {}).get("accounts", [])
    for account in accounts:
        password = account.get("password")
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
