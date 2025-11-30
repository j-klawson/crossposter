# Crosspost: Post to Mastodon, Bluesky & Twitter at the Same Time

**Crosspost** is a simple Python CLI tool that lets you post the same message to multiple **Mastodon**, **Bluesky**, and **Twitter** accounts at once.

---

## Features

- Post to multiple Mastodon, Bluesky, and Twitter accounts
- Enable/disable each service via config
- Secure **macOS Keychain** credential storage (no passwords in files)
- Single TOML config file (safe to commit to git, contains no secrets)
- Interactive setup: `crosspost --setup`
- CLI interface with support for links and Unicode
- Auto-detects and formats URLs correctly for Bluesky using rich text "facets"
- Configurable Keychain service name (defaults to "crosspost")
- Twitter text posts with URL support

---

## Installation

1. Clone this repo:

   ```bash
   git clone https://github.com/j-klawson/crosspost.git
   cd crosspost
   ```

2. Install the package:

   ```bash
   pip install .
   ```

   Or in editable/development mode:

   ```bash
   pip install -e .
   ```

---

## Configuration

### Overview

Crosspost uses **macOS Keychain** to store credentials securely. No passwords are ever stored in config files or shell history.

Your `config.toml` contains only account definitions (names, instances, handles) - not credentials.

### Configuration File

Create a `config.toml` file with your accounts. See `config.toml.example` for a template.

Safe to commit to git (contains no secrets):

```toml
[mastodon]
enabled = true

[[mastodon.accounts]]
name = "primary"
instance = "https://mastodon.social"
keychain_key = "mastodon_primary"

[bluesky]
enabled = true

[[bluesky.accounts]]
name = "main"
handle = "yourhandle.bsky.social"
keychain_key = "bluesky_main"

[twitter]
enabled = true

[[twitter.accounts]]
name = "main"
handle = "@yourhandle"
keychain_key = "twitter_main"
```

### Keychain Setup

Two options to store credentials in Keychain:

**Option 1: Interactive Setup (Recommended)**

```bash
crosspost --setup
```

This prompts you to enter credentials for all configured accounts and stores them securely in Keychain.

**Option 2: On First Run**

Simply run:

```bash
crosspost "Your post text"
```

If a credential is missing from Keychain, you'll be prompted to enter it. It's then stored automatically.

### Custom Keychain Service Name

By default, credentials are stored under the service name `"crosspost"`. To use a different service name:

```toml
keychain_service = "my-custom-service"

[[mastodon.accounts]]
name = "primary"
instance = "https://mastodon.social"
keychain_key = "mastodon_primary"
```

### Bluesky Note

Use your **app password**, not your account password. Generate one at https://bsky.app/settings/app-passwords

### Twitter Setup

To post to Twitter, you need OAuth 1.0a credentials from the Twitter Developer Portal:

1. Visit https://developer.twitter.com/en/portal/dashboard
2. Create or select an app
3. Go to the "Keys and tokens" tab and generate/copy:
   - **API Key** (consumer_key)
   - **API Secret** (consumer_secret)
   - **Access Token** (in the "Authentication Tokens" section)
   - **Access Token Secret** (in the "Authentication Tokens" section)

When you run `crosspost --setup`, you'll be prompted to enter all four credentials. They're stored securely in Keychain as a single JSON entry.

Example Twitter config:

```toml
[twitter]
enabled = true

[[twitter.accounts]]
name = "main"
handle = "@yourhandle"
keychain_key = "twitter_main"
```

### Disable Platforms

You can disable any service by setting `enabled = false`:

```toml
[mastodon]
enabled = true

[bluesky]
enabled = true

[twitter]
enabled = false
```

---

## Usage

After installation, run from anywhere with:

```bash
crosspost "Just posted a new article! https://example.com/blog"
```

### First Run

If `config.toml` is not found, crosspost will automatically create an example configuration at `~/.config/crosspost/config.toml`:

```
✨ Created example config at ~/.config/crosspost/config.toml
📝 Please edit it with your account details
🔐 Then run: crosspost --setup
```

1. Edit the config with your Mastodon instances, Bluesky handles, and Twitter handles
2. Run `crosspost --setup` to enter credentials into Keychain
3. Run `crosspost "Your post text"` to start posting


---

## Example Output

```
✅ Posted to Mastodon (primary)
✅ Posted to Mastodon (tech)
✅ Posted to Bluesky (main)
✅ Posted to Bluesky (alt)
✅ Posted to Twitter (main)
```

---

## Development

To set up a development environment:

```bash
git clone https://github.com/j-klawson/crosspost.git
cd crosspost
pip install -e .
```

The `-e` flag installs the package in editable mode, so changes to the source code are immediately reflected.

### Project Structure

```
src/crosspost/
├── __init__.py       # Package metadata and exports
├── cli.py            # Command-line interface
├── config.py         # Configuration file handling
└── poster.py         # Mastodon, Bluesky, and Twitter posting logic
```

---

## License

MIT License. See [LICENSE](LICENSE) for details.
