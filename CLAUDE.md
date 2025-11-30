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

Crosspost is a Python package for cross-posting to multiple social media platforms (Mastodon and Bluesky) simultaneously. It's now properly packaged and installable via pip.

### Key Files

- **src/crosspost/cli.py** - Entry point and CLI argument parsing
- **src/crosspost/config.py** - Handles loading config.toml files
- **src/crosspost/poster.py** - Contains posting logic for both platforms
- **pyproject.toml** - Package metadata and build configuration
- **README.md** - User-facing documentation
- **man/crosspost.1** - Man page (groff format)

## Configuration

The app looks for `config.toml` in this order:
1. Current working directory (highest priority)
2. `~/.config/crosspost/config.toml` (XDG-compliant)
3. If neither exists, auto-creates an example at `~/.config/crosspost/config.toml`

### Auto-Create on First Run

The first time you run `crosspost`, if no config file exists, it will:
1. Create `~/.config/crosspost/` directory
2. Create `config.toml` with example accounts
3. Print a message asking you to edit it with your credentials

This gives new users a clean onboarding experience without having to copy example files manually.

### Config Format

All configuration is in a single TOML file (`config.toml`). Credentials can be:
- Inlined directly in the config
- Referenced via environment variables for extra security

Example:

```toml
[mastodon]
enabled = true

[[mastodon.accounts]]
name = "primary"
instance = "https://mastodon.social"
# Inline token directly
token = "your_token_here"
# OR use environment variable
# token = { env = "MASTODON_TOKEN" }

[bluesky]
enabled = true

[[bluesky.accounts]]
name = "main"
handle = "yourhandle.bsky.social"
password = "your_app_password"
```

Note: Bluesky uses app passwords (not the regular account password). Generate these at https://bsky.app/settings/app-passwords

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
# Test with both platforms enabled
crosspost "Test post https://example.com"

# Test with only Mastodon (disable bluesky in config.toml)
# Test with only Bluesky (disable mastodon in config.toml)
```

## Known Issues & TODOs

- [ ] Add unit tests
- [ ] Handle multiple URLs in a single post more robustly (current implementation uses first occurrence)
- [ ] Add support for media attachments
- [ ] Add verbose/debug logging flag
- [ ] Add config validation/schema
- [ ] Publish to PyPI

## Future Enhancements

- Support for more platforms (Threads, LinkedIn, etc.)
- Template/scheduled posting
- Rich text formatting (bold, italic, links)
- Media uploads
- Batch posting from file

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
- **python-dotenv** >= 1.0.0 - Environment variable loading

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