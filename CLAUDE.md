# Development Notes for Crosspost

## Quick Start

```bash
# Install in editable mode (development)
pip install -e .

# Run the CLI from anywhere
crosspost "Your post text https://example.com"

# Or run directly during development
python -m crosspost.cli "Your post text"
```

## Project Overview

Crosspost is a Python package for cross-posting to multiple social media platforms (Mastodon, Bluesky, and Twitter) simultaneously. It's properly packaged and installable via pip.

### Key Files

- **src/crosspost/cli.py** - Entry point and CLI argument parsing
- **src/crosspost/config.py** - Handles loading config.toml files
- **src/crosspost/poster.py** - Contains posting logic for Mastodon, Bluesky, and Twitter
- **pyproject.toml** - Package metadata and build configuration
- **README.md** - User-facing documentation
- **man/crosspost.1** - Man page (groff format)

## Configuration

### Credential Storage with Keychain

All credentials are stored securely in **macOS Keychain** via the `keyring` library. The config file contains only account definitions (names, instances, handles) - never credentials.

### Config File Location

The app looks for `config.toml` in this order:
1. Current working directory (highest priority)
2. `~/.config/crosspost/config.toml` (XDG-compliant)
3. If neither exists, auto-creates an example at `~/.config/crosspost/config.toml`

### Auto-Create on First Run

The first time you run `crosspost`, if no config file exists, it will:
1. Create `~/.config/crosspost/` directory
2. Create `config.toml` with example accounts
3. Print instructions to run `crosspost --setup`

This gives new users a clean onboarding experience.

### Config Format

All configuration is in a single TOML file (`config.toml`). No credentials are stored here - only account definitions:

```toml
# Optional: customize Keychain service name (defaults to "crosspost")
keychain_service = "crosspost"

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

Two ways to populate Keychain:

1. **Recommended: Interactive setup**
   ```bash
   crosspost --setup
   ```
   Prompts for each account's credential and stores securely in Keychain.

2. **On first post**
   ```bash
   crosspost "Your post text"
   ```
   Missing credentials trigger interactive prompt (hidden input) and are stored in Keychain.

### Keychain Service Names

Credentials are stored with structure: `service/keychain_key`

By default, service = `"crosspost"` (customizable with `keychain_service` config key)

Example: `crosspost/mastodon_primary`, `crosspost/bluesky_main`

### Implementation Details

- **File**: `src/crosspost/config.py`
- `_get_from_keychain(service, key)` - Retrieves from Keychain
- `_prompt_for_credential(prompt_text)` - Hidden input via `getpass`
- `_resolve_credential()` - Handles lookup, prompting, and caching
- `setup_keychain(config)` - Interactive setup for all accounts
- `_credential_cache` - In-memory cache during execution (avoids repeated Keychain lookups)

### Error Handling

- If keyring library not found: hard fail with install instructions
- If credential missing: prompt user (hidden input), then store in Keychain
- If user cancels (Ctrl+C): skip that account, warn user
- All exceptions caught with user-friendly messages

Note: Bluesky requires app passwords, not account passwords. Generate at https://bsky.app/settings/app-passwords

## Man Page

A man page is included and installed automatically with the package:

```bash
man crosspost
```

The man page (man/crosspost.1) is in groff format and covers:
- Command syntax and arguments
- Configuration file format
- Environment variable usage
- Examples
- Known limitations

## Testing

Currently, there are no automated tests. To test manually:

```bash
# Test with all platforms enabled
crosspost "Test post https://example.com"

# Test with individual platforms (disable others in config.toml)
# Test with only Mastodon (set bluesky/twitter enabled = false)
# Test with only Bluesky (set mastodon/twitter enabled = false)
# Test with only Twitter (set mastodon/bluesky enabled = false)
```

## Known Issues & TODOs

- [ ] Add unit tests for all three platforms
- [ ] Handle multiple URLs in a single post more robustly (Bluesky regex approach)
- [ ] Add support for media attachments (for Mastodon, Bluesky, Twitter)
- [ ] Add verbose/debug logging flag
- [ ] Add config validation/schema
- [ ] Publish to PyPI
- [ ] Add Twitter thread support (reply chains)

## Future Enhancements

- Support for more platforms (Threads, LinkedIn, etc.)
- Template/scheduled posting
- Rich text formatting (bold, italic, links)
- Media uploads
- Batch posting from file
- Repost/RT to Twitter
- Hashtag and mention detection/expansion

## Publishing to PyPI

When ready to publish:

```bash
# Build the distribution
python -m pip install --upgrade build
python -m build

# Upload to PyPI (requires account and credentials)
python -m pip install --upgrade twine
python -m twine upload dist/*
```

## Dependencies

- **Mastodon.py** >= 1.8.0 - Mastodon API client
- **atproto** >= 0.0.40 - Bluesky/ATProto client
- **tweepy** >= 4.14.0 - Twitter API v2 client
- **keyring** >= 23.0.0 - macOS Keychain credential storage

## Architecture Notes

The code is modularized for clarity:

- **config.py**: Handles all file I/O and environment variable loading
- **poster.py**: Stateless functions for posting to each platform
- **cli.py**: Thin CLI wrapper that ties everything together

This makes it easy to import and use the posting functions programmatically in other projects.

## Bluesky URL Handling

Bluesky requires URLs to be specified using "facets" (rich text formatting). The current implementation:
1. Finds all URLs using regex: `https?://\S+`
2. Creates a facet for each URL
3. Sends post with facets parameter

This is why the README mentions "Auto-detects and formats URLs correctly for Bluesky using rich text facets".

### Caveat

If the same URL appears multiple times in a post, the current regex approach may have issues. This is a known limitation (see TODOs).

## Twitter Integration

### Credentials Storage

Twitter credentials are different from Mastodon and Bluesky because they require **four separate values** instead of just one token/password. These are OAuth 1.0a User Context credentials:

1. **API Key** (consumer_key)
2. **API Secret** (consumer_secret)
3. **Access Token**
4. **Access Token Secret**

All four are stored together as JSON in a single Keychain entry:

```json
{
  "api_key": "...",
  "api_secret": "...",
  "access_token": "...",
  "access_token_secret": "..."
}
```

### Setup Process

During `crosspost --setup`, when a Twitter account is encountered:
1. User is prompted to enter the 4 credentials (each with hidden input)
2. They're packaged as JSON
3. Stored in Keychain as a single entry (e.g., `crosspost/twitter_main`)

### Config Format

Twitter config follows the same pattern as other platforms:

```toml
[twitter]
enabled = true

[[twitter.accounts]]
name = "main"
handle = "@yourhandle"
keychain_key = "twitter_main"
```

### Implementation Details

- **Library**: `tweepy>=4.14.0` (Twitter API v2 client)
- **File**: `src/crosspost/poster.py`
- **Function**: `post_to_twitter(text, config)` - Posts text to configured Twitter accounts
- **Credential parsing**: Done in `load_config()` in `config.py`
  - `_prompt_for_twitter_credentials()` - Interactive prompting for all 3 credentials
  - JSON parsing in `load_config()` extracts api_key, api_secret, bearer_token to account dict

### API Rate Limits

Twitter API v2 has rate limits. The implementation:
- Catches `tweepy.TweepyException` for auth/API errors
- Provides user-friendly error messages
- Continues to next account on failure (doesn't exit)

### Text Posting Only

Current implementation posts text only - no media attachments. URLs are included as plain text (Twitter handles URL detection automatically).

## Local Development Tips

- Always use `pip install -e .` when developing to ensure your changes are reflected
- The CLI command `crosspost` is available globally once installed in editable mode
- The `config.toml` file is in .gitignore so secrets won't leak
- Use `config.toml.example` as a template for creating your actual config
- To view the installed man page: `man crosspost`

## Troubleshooting

**"crosspost: command not found"** after `pip install -e .`
- Ensure the virtual environment is activated or using the correct Python
- Check that the installation completed without errors
- Run `pip show crosspost` to verify it's installed

**"Error: 'config.toml' not found"**
- Ensure config.toml is in the current directory or `~/.config/crosspost/`
- Check that the file exists and is readable
- Verify the TOML syntax is valid (use a TOML validator if unsure)

**Bluesky posts fail**
- Verify the app password is correct (not the account password)
- Ensure the handle format is correct (should end in .bsky.social)
- Check that the account hasn't disabled API access

**Mastodon posts fail**
- Verify the token has proper permissions
- Check that the instance URL is correct and ends with https://
- Ensure the token hasn't expired or been revoked
- do not attempt to do git commits or write commit messages. I will do them manually.
- Never modify ~/.config/crosspost/config.toml