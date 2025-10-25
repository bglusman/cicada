# Cicada Installation Guide

## Quick Install with UV (Recommended ⚡)

The **fastest** way to install and set up Cicada using [uv](https://github.com/astral-sh/uv):

```bash
# Install and run in one command (no prior setup needed!)
cd /path/to/your/elixir/project
uvx --from git+https://github.com/YOUR_USERNAME/cicada.git cicada-setup --repo .
```

Benefits:
- ⚡ **10-100x faster** than traditional pip
- 🎯 **Single command** - downloads, installs, and configures everything
- 🔒 **Isolated** - doesn't affect your system Python
- ✨ **No cloning** required - installs directly from GitHub

Or install as a persistent tool:

```bash
# Install once
uv tool install git+https://github.com/YOUR_USERNAME/cicada.git

# Use in any project
cd /path/to/elixir/project
cicada-setup --repo .
```

### Installing UV

If you don't have uv yet:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or via Homebrew:
```bash
brew install uv
```

## Traditional Install

Without uv (slower but still works):

```bash
cd /path/to/your/elixir/project
python3 /path/to/cicada/setup.py --repo .
```

That's it! The script will:
1. Create a virtual environment (if needed)
2. Install all dependencies
3. Index your Elixir repository
4. Create `.cicada/index.json` in your project
5. Create `.mcp.json` configuration for Claude Code

## What Gets Created

After running the setup, you'll have:

```
your-project/
├── .cicada/
│   └── index.json          # Searchable index of all modules & functions
└── .mcp.json               # Claude Code MCP server configuration
```

## Options

### Basic Options

```bash
# Get help
python3 setup.py --help

# Setup a specific project
python3 setup.py --repo /path/to/elixir/project

# Skip dependency installation (if already set up)
python3 setup.py --repo . --skip-install
```

### Advanced Options

```bash
# Include PR information (requires GitHub CLI, may be slow)
python3 setup.py --repo . --pr-info

# Install to a custom directory
python3 setup.py --repo . --cicada-dir /custom/location

# Download from GitHub (if not installed locally)
python3 setup.py --repo . --github-url https://github.com/YOUR/cicada.git
```

## Using with Claude Code

After setup completes:

1. The script creates `.mcp.json` in your project root
2. Claude Code will automatically detect and use this configuration
3. Restart Claude Code if it was running

Now you can ask Claude Code:
- "What modules are in this project?"
- "Show me the functions in MyApp.User"
- "Search for the create_user function"

## Updating the Index

If your codebase changes, re-run the indexer:

```bash
# Quick re-index (uses existing installation)
python3 setup.py --repo . --skip-install

# Or use the indexer directly
python3 /path/to/cicada/cicada/indexer.py . --output .cicada/index.json
```

## Troubleshooting

### "Python 3.10+ required"

Make sure you have Python 3.10 or higher:

```bash
python3 --version
```

If not, install a newer Python version using your system package manager or [pyenv](https://github.com/pyenv/pyenv).

### "Index file not found"

The indexer failed to run. Try running it manually:

```bash
python3 /path/to/cicada/cicada/indexer.py . --output .cicada/index.json
```

### MCP Server Won't Connect

1. Check that `.mcp.json` was created in your project root
2. Verify the paths in `.mcp.json` are absolute and correct
3. Restart Claude Code
4. Check Claude Code logs for MCP connection errors

### Virtual Environment Issues

If you encounter venv issues, try:

```bash
# Remove old venv
rm -rf /path/to/cicada/venv

# Re-run setup (without --skip-install)
python3 setup.py --repo .
```

## Manual Setup

If you prefer manual setup, see the [main README](README.md#manual-setup-advanced).

## Uninstall

To remove Cicada from a project:

```bash
# Remove configuration and index
rm -rf .cicada/
rm .mcp.json

# Restart Claude Code
```

The Cicada installation itself (typically in `~/.cicada` or your project directory) can be removed separately if desired.
