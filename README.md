<div align="center">

<img src="cicada.png" alt="CICADA Logo" width="400"/>

# CICADA

### **C**ode **I**ntelligence: **C**ontextual **A**nalysis, **D**iscovery, and **A**ttribution

*Claude searches blindly. Be its guide.*

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Elixir](https://img.shields.io/badge/Elixir-Support-purple.svg)](https://elixir-lang.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

[Features](#features) •
[Installation](#installation) •
[Usage](#usage) •
[Documentation](#documentation) •
[Contributing](#contributing)

</div>

---

## Overview

CICADA is a Model Context Protocol (MCP) server that provides Claude Code with code intelligence for Elixir projects. It indexes your codebase using tree-sitter AST parsing and provides instant access to modules, functions, call sites, and PR attribution.

### Key Features

- Fast module and function search
- Call site tracking with line numbers
- PR attribution via git blame and GitHub CLI
- Tree-sitter based parsing
- MCP integration for Claude Code

---

## Features

### Core Capabilities

- **Module Search** - Search for modules by exact name with complete function listings
- **Function Discovery** - Find functions across all modules with arities and signatures
- **Call Site Analysis** - Track where functions are called with line numbers and context
- **PR Attribution** - Discover which PR introduced each module or function
- **Public/Private Tracking** - Distinguish between `def` and `defp` functions
- **Rich Metadata** - Types, guards, argument names, and documentation

### Technical Details

- Tree-sitter based AST parsing
- Handles complex Elixir patterns (aliases, guards, type specs)
- Incremental PR indexing to avoid API rate limits
- Markdown and JSON output formatting
- Excludes vendor directories (`deps/`, `_build/`)
- Configurable via `.mcp.json`

---

## Installation

### Quick Install with UV (Recommended)

Using [uv](https://github.com/astral-sh/uv):

```bash
# Install and configure in one command
cd /path/to/your/elixir/project
uvx --from git+https://github.com/YOUR_USERNAME/cicada.git cicada-setup --repo .
```

Or install as a persistent tool:

```bash
# Install once
uv tool install git+https://github.com/YOUR_USERNAME/cicada.git

# Use in any project
cd /path/to/elixir/project
cicada-setup --repo .
```

### Traditional Install

Without uv:

```bash
cd /path/to/your/elixir/project
python3 /path/to/cicada/install.py --repo .
```

### Manual Setup

For full control:

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/cicada.git
cd cicada

# Install dependencies
pip install -r requirements.txt

# Index your Elixir project
python -m cicada.indexer --repo /path/to/your/elixir/project

# Configure for Claude Code (see Configuration section)
```

See [INSTALL.md](INSTALL.md) for detailed installation instructions.

---

## Quick Start

After installation, ask Claude Code:

```
"What functions are in the MyApp.User module?"
"Show me where authenticate/2 is called"
"Which PR introduced the Accounts module?"
"Find all usages of Repo.insert/2"
```

---

## Usage

### Available MCP Tools

#### `search_module`

Search for a module by exact name and retrieve all its functions.

**Example:**
```
User: "Show me the MyApp.User module"
```

**Returns:**
- Module location (file path and line number)
- All functions with arities, signatures, and types
- Public vs private function counts
- Optional PR information

#### `search_function`

Search for functions across all modules with optional call site tracking.

**Parameters:**
- `function_name` - Function to search (supports multiple formats)
- `include_usage_examples` - Show actual code snippets from call sites
- `max_examples` - Limit number of usage examples (default: 5)
- `test_files_only` - Only show calls from test files

**Example:**
```
User: "Find all usages of create_user with examples"
```

**Returns:**
- Function definitions with full signatures
- Call sites with file paths and line numbers
- Optional code snippets showing usage
- PR attribution for each function

#### `find_pr_for_line`

Discover which pull request introduced a specific line of code.

**Parameters:**
- `file_path` - Path to the file
- `line_number` - Line number to investigate
- `format` - Output format (text, json, or markdown)

**Example:**
```
User: "Which PR added line 42 in lib/myapp/user.ex?"
```

**Returns:**
- Commit information
- PR number, title, and URL
- Author details
- Merge date

---

## Architecture

```
┌─────────────────────────────────────────┐
│           Claude Code (Client)          │
└────────────────┬────────────────────────┘
                 │ MCP Protocol
┌────────────────▼────────────────────────┐
│       CICADA MCP Server                 │
│  • search_module                        │
│  • search_function                      │
│  • find_pr_for_line                     │
└───┬─────────────┬────────────┬──────────┘
    │             │            │
┌───▼──────┐  ┌──▼─────┐  ┌───▼────────┐
│ Parser   │  │ Indexer│  │ PR Finder  │
│          │  │        │  │            │
└───┬──────┘  └──┬─────┘  └───┬────────┘
    │            │             │
    └────────┬───┴─────────────┘
             │
        ┌────▼─────┐
        │.cicada/  │
        │index.json│
        └──────────┘
```

---

## Index Structure

```json
{
  "modules": {
    "MyApp.User": {
      "file": "lib/myapp/user.ex",
      "line": 1,
      "functions": [
        {
          "name": "authenticate",
          "arity": 2,
          "full_name": "authenticate/2",
          "line": 42,
          "signature": "def authenticate(email, password)",
          "type": "def",
          "arguments": ["email", "password"]
        }
      ],
      "total_functions": 5,
      "public_functions": 3,
      "private_functions": 2,
      "pr_info": {
        "number": 45,
        "title": "Add user authentication",
        "author": "jane-doe",
        "merged_at": "2024-10-15T10:30:00Z"
      }
    }
  },
  "metadata": {
    "indexed_at": "2025-10-25T10:30:00",
    "total_modules": 45,
    "total_functions": 320,
    "repo_path": "/path/to/repo"
  }
}
```

---

## Configuration

### Project Configuration (`.mcp.json`)

Created automatically by the setup script:

```json
{
  "mcpServers": {
    "cicada": {
      "command": "python",
      "args": ["/absolute/path/to/cicada/cicada/mcp_server.py"],
      "cwd": "/absolute/path/to/cicada",
      "env": {
        "CICADA_INDEX_PATH": "/path/to/project/.cicada/index.json"
      }
    }
  }
}
```

### Setup Options

```bash
# Basic setup
cicada-setup --repo .

# Include PR information (requires GitHub CLI)
cicada-setup --repo . --pr-info

# Skip dependency installation
cicada-setup --repo . --skip-install

# Custom installation directory
cicada-setup --repo . --cicada-dir /custom/path
```

---

## Documentation

### Components

- **Parser** (`cicada/parser.py`) - Tree-sitter Elixir parser extracting modules, functions, and metadata
- **Indexer** (`cicada/indexer.py`) - Repository crawler building searchable indexes
- **MCP Server** (`cicada/mcp_server.py`) - Model Context Protocol server exposing search tools
- **PR Finder** (`cicada/pr_finder.py`) - Git blame and GitHub CLI integration for PR attribution
- **Formatter** (`cicada/formatter.py`) - Output formatting for markdown and JSON

### Advanced Usage

#### Re-indexing

After code changes, re-index your project:

```bash
# Quick re-index (uses existing installation)
cicada-setup --repo . --skip-install

# Or use the indexer directly
cicada-index --repo . --output .cicada/index.json
```

#### PR Indexing

Build a comprehensive PR cache to avoid GitHub API rate limits:

```bash
cicada-index --repo . --fetch-pr-info
```

#### Custom Index Location

```bash
cicada-index --repo /path/to/project --output /custom/location/index.json
```

---

## Testing

Run the test suite:

```bash
# Install test dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run specific test files
pytest tests/test_parser.py
pytest tests/test_search_function.py

# Run with coverage
pytest --cov=cicada --cov-report=html
```

### Test Coverage

- Parser: Elixir syntax, modules, functions, arguments, types
- Indexer: Repository walking, exclusions, metadata generation
- MCP Server: Tool invocation, search results, formatting
- PR Finder: Git blame, PR attribution, caching
- Call Sites: Function usage tracking, code snippets

---

## Roadmap

### v0 (Current)
- Module and function search
- Call site tracking
- PR attribution
- Basic MCP integration

### v0.1 (Planned)
- Enhanced test detection with confidence scoring
- Documentation search in markdown files
- Git commit history integration
- Usage pattern extraction

### v0.2 (Future)
- Comprehensive context aggregation
- Implementation guidance (error patterns, conventions)
- Improved fuzzy search capabilities
- Multi-repository support

### Long Term
- Multi-language support (Python, TypeScript, Rust)
- Semantic code search
- Real-time incremental indexing
- Web UI for exploration

---

## Limitations (v0)

Current limitations:
- Exact match only (no fuzzy search)
- Direct call tracking only (not comprehensive call graphs)
- No automatic documentation file search
- No function similarity suggestions
- No usage convention extraction

These features may be added in future versions.

---

## Contributing

### Getting Started

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Commit your changes
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/cicada.git
cd cicada

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with test dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

### Code Style

This project uses:
- **black** for code formatting
- **pytest** for testing
- **type hints** where appropriate

Before submitting a PR:
```bash
# Format code
black cicada tests

# Run tests
pytest

# Check types (if using mypy)
mypy cicada
```

### Reporting Issues

When reporting bugs or requesting features:

1. Check existing [Issues](https://github.com/YOUR_USERNAME/cicada/issues)
2. If not found, create a new issue with:
   - Clear description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Your environment (OS, Python version, Elixir version)

---

## Troubleshooting

### "Index file not found"

Run the indexer first:
```bash
cicada-index --repo /path/to/project
```

### "Module not found"

Use the exact module name as it appears in code (e.g., `MyApp.User`, not `User`).

### MCP Server Won't Connect

1. Verify `.mcp.json` exists in your project root
2. Check that all paths in `.mcp.json` are absolute
3. Ensure `index.json` was created successfully
4. Restart Claude Code
5. Check Claude Code logs for errors

### PR Information Not Working

PR attribution requires GitHub CLI:
```bash
# Install GitHub CLI
brew install gh  # macOS
# or visit https://cli.github.com/

# Authenticate
gh auth login

# Re-run indexer with PR info
cicada-index --repo . --fetch-pr-info
```

---

## Project Structure

```
cicada/
├── cicada/                # Main package
│   ├── __init__.py
│   ├── parser.py          # Tree-sitter Elixir parser
│   ├── indexer.py         # Repository indexer
│   ├── mcp_server.py      # MCP server implementation
│   ├── formatter.py       # Output formatting
│   ├── pr_finder.py       # PR attribution
│   └── pr_indexer.py      # PR cache builder
├── tests/                 # Test suite
│   ├── test_parser.py
│   ├── test_search_function.py
│   ├── test_call_sites.py
│   └── ...
├── docs/                  # Documentation
│   └── WEEKEND_MVP_PLAN.md
├── install.py             # Setup script
├── pyproject.toml         # Project configuration
├── requirements.txt       # Dependencies
├── README.md              # This file
├── INSTALL.md             # Installation guide
└── LICENSE                # MIT License
```

---

## Credits

### Built With

- [Tree-sitter](https://tree-sitter.github.io/) - Incremental parsing system
- [tree-sitter-elixir](https://github.com/elixir-lang/tree-sitter-elixir) - Elixir grammar
- [MCP](https://modelcontextprotocol.io/) - Model Context Protocol
- [GitHub CLI](https://cli.github.com/) - PR attribution

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- The Anthropic team for Claude Code and MCP
- The Elixir community for tree-sitter-elixir
- All contributors who help improve CICADA

---

<div align="center">

**[⬆ back to top](#cicada)**

</div>
