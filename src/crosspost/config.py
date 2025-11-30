"""Configuration loading for crosspost."""

import os
import sys
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib


# Example configuration embedded for auto-creation
EXAMPLE_CONFIG = """# Crosspost Configuration
# Fill in your credentials below
# Keep this file private - never commit it!

[mastodon]
enabled = true

# Define Mastodon accounts to post to
[[mastodon.accounts]]
name = "primary"
instance = "https://mastodon.social"
# Inline the token directly:
token = "your_mastodon_token_here"

# Or reference an environment variable:
# token = { env = "MASTODON_TOKEN_1" }

[[mastodon.accounts]]
name = "fosstodon"
instance = "https://fosstodon.org"
token = "your_second_token_here"

[bluesky]
enabled = true

# Define Bluesky accounts to post to
# Note: Use your Bluesky app password, NOT your account password
# Generate at: https://bsky.app/settings/app-passwords

[[bluesky.accounts]]
name = "main"
handle = "yourhandle.bsky.social"
# Inline the password directly:
password = "xxxx-xxxx-xxxx-xxxx"

# Or reference an environment variable:
# password = { env = "BLUESKY_PASS_1" }

[[bluesky.accounts]]
name = "alt"
handle = "althandle.bsky.social"
password = "yyyy-yyyy-yyyy-yyyy"
"""


def find_config_file():
    """Find the config file, checking multiple locations.

    If no config exists, creates an example at ~/.config/crosspost/config.toml

    Returns:
        Path: Path to the config file

    Raises:
        SystemExit: If config file creation fails
    """
    # Check current directory first
    config_path = Path("config.toml")
    if config_path.exists():
        return config_path

    # Check ~/.config/crosspost (XDG-style)
    xdg_config = Path.home() / ".config" / "crosspost" / "config.toml"
    if xdg_config.exists():
        return xdg_config

    # Create example config
    try:
        xdg_config.parent.mkdir(parents=True, exist_ok=True)
        xdg_config.write_text(EXAMPLE_CONFIG)
        print(f"✨ Created example config at {xdg_config}")
        print("📝 Please edit it with your credentials and run crosspost again")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error creating config at {xdg_config}: {e}")
        sys.exit(1)


def _resolve_secret(value):
    """Resolve a secret value, supporting both inline secrets and environment variable references.

    Args:
        value: Either a direct secret string or a dict with 'env' key for env var reference

    Returns:
        str: The resolved secret value
    """
    if isinstance(value, str):
        return value
    elif isinstance(value, dict) and "env" in value:
        env_var = value["env"]
        secret = os.getenv(env_var)
        if not secret:
            print(f"⚠️ Warning: Environment variable '{env_var}' not set")
        return secret
    return None


def load_config():
    """Load configuration from config.toml file.

    Returns:
        dict: Configuration dictionary with 'mastodon' and 'bluesky' keys

    Raises:
        SystemExit: If config file not found or invalid
    """
    config_path = find_config_file()

    try:
        with open(config_path, "rb") as f:
            config = tomllib.load(f)
    except Exception as e:
        print(f"❌ Error parsing 'config.toml': {e}")
        sys.exit(1)

    # Resolve any environment variable references in credentials
    for platform in ["mastodon", "bluesky"]:
        if platform not in config:
            continue

        accounts = config[platform].get("accounts", [])
        for account in accounts:
            # Handle Mastodon token
            if "token" in account:
                account["token"] = _resolve_secret(account["token"])
            # Handle Bluesky password
            if "password" in account:
                account["password"] = _resolve_secret(account["password"])

    return config
