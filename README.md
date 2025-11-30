# Crosspost: Post to Mastodon & Bluesky at the Same Time

**Crosspost** is a simple Python CLI tool that lets you post the same message to multiple **Mastodon** and **Bluesky** accounts at once.

---

## Features

- Post to multiple Mastodon and Bluesky accounts
- Enable/disable either service via config
- Secure **macOS Keychain** credential storage (no passwords in files)
- Single TOML config file (safe to commit to git, contains no secrets)
- Interactive setup: `crosspost --setup`
- CLI interface with support for links and Unicode
- Auto-detects and formats URLs correctly for Bluesky using rich text "facets"
- Configurable Keychain service name (defaults to "crosspost")

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

### Disable Platforms

You can disable either service by setting `enabled = false`:

```toml
[mastodon]
enabled = false

[bluesky]
enabled = true
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

1. Edit the config with your Mastodon instances and Bluesky handles
2. Run `crosspost --setup` to enter credentials into Keychain
3. Run `crosspost "Your post text"` to start posting


---

## Example Output

```
✅ Posted to Mastodon (primary)
✅ Posted to Mastodon (tech)
✅ Posted to Bluesky (main)
✅ Posted to Bluesky (alt)
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
└── poster.py         # Mastodon and Bluesky posting logic
```

---

## License

MIT License. See [LICENSE](LICENSE) for details.
