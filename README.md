# 📰 Crosspost: Post to Mastodon & Bluesky at the Same Time

**Crosspost** is a simple Python CLI tool that lets you post the same message to multiple **Mastodon** and **Bluesky** accounts at once.

Ideal for developers, bloggers, or bots who want to reach both networks without copy-pasting.

---

## Features

- ✅ Post to multiple Mastodon and Bluesky accounts
- ✅ Enable/disable either service via config
- ✅ Reads secrets from `.env` file
- ✅ CLI interface with support for links and Unicode
- ✅ Auto-detects and formats URLs correctly for Bluesky using rich text "facets"

---

## 📦 Installation

1. Clone this repo:

   ```bash
   git clone https://github.com/yourusername/crosspost.git
   cd crosspost
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## ⚙️ Configuration

### 1. `config.env`

Store credentials here (never commit it!).

```env
# Mastodon tokens
MASTODON_TOKEN_1=your_mastodon_access_token

# Bluesky credentials
BLUESKY_HANDLE=your-handle.bsky.social
BLUESKY_PASS_1=abcd-efgh-ijkl-mnop
```

### 2. `config.json`

Define which accounts to use:

```json
{
  "mastodon": {
    "enabled": true,
    "accounts": [
      {
        "name": "primary",
        "instance": "https://mastodon.social",
        "token_env": "MASTODON_TOKEN_1"
      }
    ]
  },
  "bluesky": {
    "enabled": true,
    "accounts": [
      {
        "name": "main",
        "handle": "your-handle.bsky.social",
        "password_env": "BLUESKY_PASS_1"
      }
    ]
  }
}
```

---

## Usage

Run from the terminal:

```bash
./crosspost.py "Just posted a new article! https://example.com/blog"
```

---

## Example Output

```
✅ Posted to Mastodon (primary)
✅ Posted to Bluesky (main) with link facets
```

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Contributing

Pull requests are welcome.

