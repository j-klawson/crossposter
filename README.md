# Crosspost: Post to Mastodon & Bluesky at the Same Time

**Crosspost** is a simple Python CLI tool that lets you post the same message to multiple **Mastodon** and **Bluesky** accounts at once.

Ideal for developers, bloggers, or bots who want to reach both networks without copy-pasting.

---

## Features

- Post to multiple Mastodon and Bluesky accounts
- Enable/disable either service via config
- Single TOML config file (easy to maintain, all-in-one)
- CLI interface with support for links and Unicode
- Auto-detects and formats URLs correctly for Bluesky using rich text "facets"
- Supports both inline credentials and environment variable references

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

### Configuration File

Create a `config.toml` file with your accounts and credentials. See `config.toml.example` for a template.

**Important**: Keep `config.toml` in `.gitignore` and never commit it - it contains secrets!

### Basic Example

```toml
[mastodon]
enabled = true

[[mastodon.accounts]]
name = "primary"
instance = "https://mastodon.social"
token = "your_token_here"

[bluesky]
enabled = true

[[bluesky.accounts]]
name = "main"
handle = "yourhandle.bsky.social"
password = "your_app_password_here"
```

### Using Environment Variables

For added security, you can reference environment variables instead of inline secrets:

```toml
[[mastodon.accounts]]
name = "primary"
instance = "https://mastodon.social"
token = { env = "MASTODON_TOKEN" }

[[bluesky.accounts]]
name = "main"
handle = "yourhandle.bsky.social"
password = { env = "BLUESKY_PASS" }
```

Then set the environment variables before running:

```bash
export MASTODON_TOKEN="your_token"
export BLUESKY_PASS="your_app_password"
crosspost "Your post text"
```

### Disable Platforms

You can disable either service by setting `enabled = false`:

```toml
[mastodon]
enabled = false

[bluesky]
enabled = true
```

### Bluesky Note

Use your **app password**, not your account password. Generate one at https://bsky.app/settings/app-passwords

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
📝 Please edit it with your credentials and run crosspost again
```

Edit the file with your Mastodon tokens and Bluesky app passwords, then run the command again.


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