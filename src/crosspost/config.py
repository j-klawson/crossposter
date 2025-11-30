"""Configuration loading for crosspost with secure Keychain credential storage."""

import sys
import getpass
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib

try:
    import keyring
except ImportError:
    print("❌ Error: keyring library not available.")
    print("   Install it with: pip install keyring")
    sys.exit(1)


# Example configuration embedded for auto-creation
EXAMPLE_CONFIG = """# Crosspost Configuration
# Credentials are stored securely in macOS Keychain
# This file is safe to commit to git (contains no secrets)
#
# Setup:
# 1. Edit this file with your account definitions (no credentials needed)
# 2. Run: crosspost --setup
# 3. Follow prompts to enter credentials, which are stored in Keychain

# Optional: customize the Keychain service name (defaults to "crosspost")
# keychain_service = "my-custom-service"

[mastodon]
enabled = true

# Define Mastodon accounts to post to
[[mastodon.accounts]]
name = "primary"
instance = "https://mastodon.social"
keychain_key = "mastodon_primary"

[[mastodon.accounts]]
name = "fosstodon"
instance = "https://fosstodon.org"
keychain_key = "mastodon_fosstodon"

[bluesky]
enabled = true

# Define Bluesky accounts to post to
# Note: Use your Bluesky app password, NOT your account password
# Generate app password at: https://bsky.app/settings/app-passwords

[[bluesky.accounts]]
name = "main"
handle = "yourhandle.bsky.social"
keychain_key = "bluesky_main"

[[bluesky.accounts]]
name = "alt"
handle = "althandle.bsky.social"
keychain_key = "bluesky_alt"
"""

# Credential cache for the current run (avoid repeated keychain lookups)
_credential_cache = {}


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
        print("📝 Please edit it with your account details")
        print("🔐 Then run: crosspost --setup")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error creating config at {xdg_config}: {e}")
        sys.exit(1)


def _get_from_keychain(service, key):
    """Get a credential from Keychain.

    Args:
        service (str): Keychain service name
        key (str): Credential key/username

    Returns:
        str: The credential value, or None if not found
    """
    try:
        return keyring.get_password(service, key)
    except Exception as e:
        print(f"⚠️ Keychain error: {e}")
        return None


def _prompt_for_credential(prompt_text):
    """Prompt user for a credential with hidden input.

    Args:
        prompt_text (str): Text to display to user

    Returns:
        str: The entered credential, or None if user cancelled
    """
    try:
        return getpass.getpass(prompt_text)
    except KeyboardInterrupt:
        print("\n⏭️  Skipping...")
        return None


def _resolve_credential(service, account_name, platform_name, keychain_key):
    """Resolve a credential from Keychain, prompting if missing.

    Args:
        service (str): Keychain service name
        account_name (str): Human-readable account name
        platform_name (str): Platform name (Mastodon/Bluesky)
        keychain_key (str): Keychain key to use

    Returns:
        str: The credential, or None if not available
    """
    cache_key = f"{service}:{keychain_key}"

    # Check cache first
    if cache_key in _credential_cache:
        return _credential_cache[cache_key]

    # Try to get from keychain
    credential = _get_from_keychain(service, keychain_key)
    if credential:
        _credential_cache[cache_key] = credential
        return credential

    # Prompt user
    prompt = f"⚠️ {platform_name} credential not in Keychain\n"
    prompt += f"Enter token for '{account_name}' (or press Ctrl+C to skip): "

    credential = _prompt_for_credential(prompt)
    if not credential:
        return None

    # Store in keychain
    try:
        keyring.set_password(service, keychain_key, credential)
        print(f"✅ Saved to Keychain as '{service}/{keychain_key}'")
        _credential_cache[cache_key] = credential
        return credential
    except Exception as e:
        print(f"❌ Failed to save to Keychain: {e}")
        return None


def load_config():
    """Load configuration from config.toml file.

    Resolves credentials from Keychain, prompting if needed.

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

    # Get keychain service name from config (default: "crosspost")
    service = config.get("keychain_service", "crosspost")

    # Resolve credentials from Keychain
    for platform in ["mastodon", "bluesky"]:
        if platform not in config:
            continue

        accounts = config[platform].get("accounts", [])
        for account in accounts:
            if platform == "mastodon":
                if "keychain_key" in account:
                    account["token"] = _resolve_credential(
                        service,
                        account["name"],
                        "Mastodon",
                        account["keychain_key"]
                    )
            elif platform == "bluesky":
                if "keychain_key" in account:
                    account["password"] = _resolve_credential(
                        service,
                        account["name"],
                        "Bluesky",
                        account["keychain_key"]
                    )

    return config


def setup_keychain(config):
    """Interactive setup to pre-populate Keychain with credentials.

    Args:
        config (dict): Configuration dictionary from load_config()
    """
    service = config.get("keychain_service", "crosspost")

    print(f"\n🔐 Setting up Keychain credentials for service: '{service}'")
    print("=" * 60)

    for platform in ["mastodon", "bluesky"]:
        if platform not in config:
            continue

        if not config[platform].get("enabled", False):
            print(f"\n⏭️  {platform.capitalize()} is disabled, skipping...")
            continue

        accounts = config[platform].get("accounts", [])
        for account in accounts:
            if "keychain_key" not in account:
                continue

            keychain_key = account["keychain_key"]

            # Check if already exists
            existing = _get_from_keychain(service, keychain_key)
            if existing:
                skip = input(
                    f"\n✅ Credential already exists for '{account['name']}'. Skip? [Y/n]: "
                ).lower()
                if skip != "n":
                    continue

            # Prompt for credential
            platform_display = "Mastodon" if platform == "mastodon" else "Bluesky"
            prompt = f"\nEnter {platform_display} credential for '{account['name']}': "
            credential = _prompt_for_credential(prompt)

            if not credential:
                print(f"⏭️  Skipped '{account['name']}'")
                continue

            # Store in keychain
            try:
                keyring.set_password(service, keychain_key, credential)
                print(f"✅ Saved '{account['name']}' to Keychain")
            except Exception as e:
                print(f"❌ Failed to save '{account['name']}': {e}")

    print("\n" + "=" * 60)
    print("✨ Setup complete!")
