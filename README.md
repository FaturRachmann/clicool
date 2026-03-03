# CLICOOL

> **Make your terminal look like it owns the system.**

[![PyPI version](https://img.shields.io/pypi/v/clicool.svg)](https://pypi.org/project/clicool/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/github/actions/workflow/status/trustlabs/clicool/test.yml?branch=main)](https://github.com/trustlabs/clicool/actions)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**CLICOOL** adalah modern terminal theme & profile engine yang mengubah terminal Anda menjadi workspace yang beautiful, productive, dan personalized.

![Cyberpunk Theme](https://via.placeholder.com/800x400/0d1117/00ffff?text=CLICOOL+Cyberpunk+Theme)

---

## 🌟 Why CLICOOL?

| Problem | CLICOOL Solution |
|---------|------------------|
| Terminal membosankan | 5+ themes siap pakai |
| Config ribet | One-command enable/disable |
| Takut rusak config | Auto-backup & rollback |
| Butuh info real-time | Widget system (git, k8s, docker) |
| Setup berulang | Profile system untuk sync |

---

## ✨ Features

### Core Features

- 🎨 **5 Built-in Themes** - Cyberpunk, Matrix, Retro, Minimal, DevOps
- 🧅 **Layer System** - Modular add-ons untuk git, k8s, docker, AWS
- 🛡️ **Safety First** - Automatic backups, marker-based injection, rollback
- 🐚 **Multi-Shell** - Bash, Zsh, Fish support
- 🖥️ **Cross-Platform** - Linux, macOS, WSL2
- ⚡ **Blazing Fast** - <50ms prompt render time
- 🔌 **Extensible** - Plugin system ready

### Advanced Features

- 🎬 **Banner Animations** - Typewriter, glitch, matrix effects
- 📊 **Widget System** - Real-time info: git, k8s, docker, aws, battery, weather
- 👤 **Profile System** - Save & sync complete setups
- 🎯 **Smart Detection** - Auto-detect shell, terminal, fonts
- 🎨 **True Color** - 24-bit RGB color support
- 🔍 **Doctor Command** - Comprehensive environment diagnostics

---

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI (recommended)
pip install clicool

# Install from source
git clone https://github.com/trustlabs/clicool.git
cd clicool
pip install -e .

# Install with dev dependencies
pip install -e ".[dev]"
```

### First Time Setup

```bash
# 1. Initialize clicool
clicool init

# 2. Check your environment
clicool doctor

# 3. List available themes
clicool list

# 4. Preview a theme
clicool preview cyberpunk

# 5. Enable theme
clicool enable cyberpunk

# 6. Restart terminal or reload shell
source ~/.bashrc  # or ~/.zshrc
```

### That's It! 🎉

Your terminal is now transformed with a beautiful cyberpunk theme!

---

## 📋 Complete Command Reference

### Theme Commands

| Command | Aliases | Description | Example |
|---------|---------|-------------|---------|
| `clicool enable <theme>` | - | Enable a theme | `clicool enable cyberpunk` |
| `clicool enable --random` | `-r` | Enable random theme | `clicool enable -r` |
| `clicool enable <theme> --preview` | `-p` | Preview before apply | `clicool enable matrix -p` |
| `clicool enable <theme> --dry-run` | `-n` | Show changes | `clicool enable retro -n` |
| `clicool enable <theme> --layer <layer>` | `-l` | Add layer | `clicool enable cyberpunk -l git-status` |
| `clicool disable` | - | Disable current theme | `clicool disable` |
| `clicool disable --rollback` | `-r` | Disable + rollback | `clicool disable -r` |
| `clicool list` | - | List themes | `clicool list` |
| `clicool list --installed` | `-i` | List installed only | `clicool list -i` |
| `clicool list --layers` | `-l` | List layers | `clicool list -l` |
| `clicool list --remote` | `-r` | Browse remote | `clicool list -r` |
| `clicool preview <theme>` | - | Preview theme | `clicool preview devops` |
| `clicool search <query>` | - | Search themes | `clicool search cyber` |

### Layer Commands

```bash
# Enable theme with multiple layers
clicool enable cyberpunk --layer git-status --layer k8s-context

# Add layer to existing setup (coming soon)
clicool layer add docker-info

# Remove layer (coming soon)
clicool layer remove aws-profile

# List active layers (coming soon)
clicool layer list
```

### Safety & Diagnostics

| Command | Options | Description |
|---------|---------|-------------|
| `clicool doctor` | `--verbose`, `--fix` | Check environment health |
| `clicool backup` | `--list` | Create or list backups |
| `clicool restore` | `--list`, `<backup_id>` | Restore from backup |
| `clicool diff` | - | Show config changes |
| `clicool status` | - | Show current theme status |

### Profile Management

```bash
# Save current setup
clicool profile save my-dev-setup

# Load saved profile
clicool profile load my-dev-setup

# List profiles
clicool profile list

# Delete profile
clicool profile delete my-dev-setup

# Export profile (coming soon)
clicool profile export my-dev-setup.zip

# Import profile (coming soon)
clicool profile import my-dev-setup.zip
```

### Advanced Commands

```bash
# Initialize clicool
clicool init

# Clear theme cache
clicool cache clear

# Validate theme JSON
clicool theme validate path/to/theme.json

# Create new theme scaffold (coming soon)
clicool theme new my-theme

# Plugin management (coming soon)
clicool plugin install <plugin>
clicool plugin list
```

---

## 🎨 Built-in Themes

### Cyberpunk
**Neon-soaked futuristic theme for night owls**

```
⚡ dev@machine:~/projects/clicool (main) λ
```

- **Colors:** Cyan, Magenta, Yellow neon
- **Best for:** Night coding, cyberpunk aesthetic
- **Font:** JetBrainsMono Nerd Font

### Matrix
**Classic hacker green on black**

```
👾 neo@nebuchadnezzar:~/matrix (master) $
```

- **Colors:** Green on black
- **Best for:** Hacker aesthetic, minimal distractions
- **Font:** Any monospace

### Retro
**Amber CRT monitor vibes from the 80s**

```
💾 user@retro:~/projects (dev) >
```

- **Colors:** Amber on dark
- **Best for:** Vintage lovers, warm tones
- **Font:** VT323 or similar

### Minimal
**Clean and subtle - less is more**

```
~/projects/clicool ±
```

- **Colors:** Grayscale with blue accents
- **Best for:** Professional settings, minimal distractions
- **Font:** Any clean monospace

### DevOps Pro
**For SREs and Platform Engineers**

```
👤 dev ~/projects ☸️ prod-cluster 🐳 5 λ
```

- **Colors:** Blue, green, purple
- **Best for:** DevOps, SRE, cloud engineers
- **Widgets:** Git, K8s, Docker, AWS
- **Font:** JetBrainsMono Nerd Font

---

## 🧅 Layer System

Layers are modular add-ons that enhance your prompt with real-time information.

### Available Layers

| Layer | Description | Performance | Example Output |
|-------|-------------|-------------|----------------|
| `git-status` | Git branch + status | ~50ms | `(main) ✗` |
| `k8s-context` | Kubernetes context | ~100ms | `☸️ prod/us-east` |
| `docker-info` | Container count | ~80ms | `🐳 5` |
| `aws-profile` | AWS profile/region | ~10ms | `☁️ prod@us-east-1` |

### Using Layers

```bash
# Single layer
clicool enable cyberpunk --layer git-status

# Multiple layers
clicool enable devops --layer git-status --layer k8s-context --layer docker-info

# Stack on existing theme
clicool enable minimal --layer git-status --layer aws-profile
```

---

## 📊 Widget System

Widgets display real-time information in your prompt.

### Built-in Widgets

| Widget | Description | Update | Example |
|--------|-------------|--------|---------|
| `git` | Branch + status | Real-time | `(main) ✗` |
| `time` | Current time | Real-time | `14:30:25` |
| `exit-code` | Last command status | Real-time | `❌ 1` |
| `k8s-context` | Kubernetes context | Per-command | `☸️ prod` |
| `docker-status` | Container count | Per-command | `🐳 5` |
| `aws-profile` | AWS profile | Per-command | `☁️ prod` |
| `venv` | Python virtualenv | Real-time | `🐍 venv` |
| `node-version` | Node.js version | Per-command | `⬢ v18.0.0` |

### Widget Configuration

Configure widgets in `~/.clicool/config.json`:

```json
{
  "widgets": [
    {
      "name": "git",
      "enabled": true,
      "config": {
        "show_ahead_behind": true,
        "show_stash": true
      }
    },
    {
      "name": "time",
      "enabled": true,
      "config": {
        "format": "24h",
        "show_seconds": true
      }
    }
  ]
}
```

---

## 🛡️ Safety Features

### How We Protect Your Config

1. **Marker-based Injection**
   ```bash
   # >>> CLICOOL START: cyberpunk >>>
   # Generated config here
   # <<< CLICOOL END: cyberpunk <<<
   ```
   Only modifies content between markers, never touches your custom config.

2. **Automatic Backups**
   ```
   ~/.clicool/backups/
   ├── bashrc_20260303_143022.bak
   ├── zshrc_20260303_143022.bak
   └── metadata.json
   ```

3. **Dry-run Mode**
   ```bash
   clicool enable cyberpunk --dry-run
   # Shows what would change without modifying anything
   ```

4. **Rollback Support**
   ```bash
   clicool disable --rollback
   # Restores previous backup automatically
   ```

5. **Checksum Validation**
   Every backup is verified with SHA256 checksums.

---

## ⚙️ Configuration

### Config File Location

`~/.clicool/config.json`

### Full Configuration Example

```json
{
  "active_theme": "cyberpunk",
  "active_layers": ["git-status", "k8s-context"],
  "active_widgets": ["git", "time", "exit-code"],
  
  "auto_backup": true,
  "enable_animations": true,
  "animation_style": "typewriter",
  
  "dry_run": false,
  "verbose": false,
  "check_updates": true,
  
  "max_backups": 10,
  "marketplace_url": "https://clicool.dev/api/themes",
  
  "custom_variables": {
    "MY_VAR": "custom_value"
  }
}
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `active_theme` | string | `null` | Currently active theme |
| `active_layers` | array | `[]` | Active layer names |
| `auto_backup` | boolean | `true` | Auto backup before changes |
| `enable_animations` | boolean | `true` | Enable banner animations |
| `animation_style` | string | `"typewriter"` | Animation style |
| `dry_run` | boolean | `false` | Global dry-run mode |
| `verbose` | boolean | `false` | Verbose output |
| `max_backups` | integer | `10` | Max backups to keep |

---

## 🏗️ Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────┐
│                    User Command                          │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                   CLI Engine (Typer)                     │
└─────────────────────────────────────────────────────────┘
                          ↓
        ┌─────────────────┴─────────────────┐
        ↓                                   ↓
┌──────────────────┐              ┌──────────────────┐
│  Shell Detector  │              │  Terminal Probe  │
│  (bash/zsh/fish) │              │  (colors/fonts)  │
└──────────────────┘              └──────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                  Theme Engine                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Theme Loader │  │ Layer System │  │ Widget Mgr   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                  Safety Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Backup Mgr   │  │ Diff Check   │  │ Rollback     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Project Structure

```
clicool/
│
├── clicool/                      # Main package
│   ├── __init__.py              # Package info & constants
│   ├── __main__.py              # Entry point
│   ├── cli.py                   # CLI commands (457 lines)
│   ├── config.py                # Configuration management
│   │
│   ├── core/                    # Core functionality
│   │   ├── shell.py             # Shell detection
│   │   ├── terminal.py          # Terminal emulator detection
│   │   ├── theme_loader.py      # Theme JSON parser
│   │   ├── injector.py          # Config injection engine
│   │   ├── generator.py         # PS1 prompt generator
│   │   └── validator.py         # Schema validation
│   │
│   ├── safety/                  # Safety features
│   │   ├── backup.py            # Backup manager
│   │   ├── rollback.py          # Rollback engine
│   │   └── diff.py              # Config diff viewer
│   │
│   ├── features/                # User features
│   │   ├── doctor.py            # Environment diagnostics
│   │   ├── preview.py           # Theme preview renderer
│   │   ├── layers.py            # Layer system
│   │   ├── widgets.py           # Terminal widgets
│   │   └── animations.py        # Banner animations
│   │
│   ├── utils/                   # Utilities
│   │   ├── colors.py            # Color utilities
│   │   ├── fonts.py             # Font detection
│   │   ├── templates.py         # Template engine
│   │   └── logging.py           # Structured logging
│   │
│   └── plugins/                 # Plugin system (WIP)
│   └── profiles/                # Profile management (WIP)
│
├── themes/
│   ├── builtin/                 # Built-in themes
│   │   ├── cyberpunk.json
│   │   ├── matrix.json
│   │   ├── retro.json
│   │   ├── minimal.json
│   │   └── devops.json
│   ├── layers/                  # Layer themes
│   │   ├── git-status.json
│   │   ├── k8s-context.json
│   │   ├── docker-info.json
│   │   └── aws-profile.json
│   └── community/               # Downloaded themes
│
├── templates/
│   ├── bash/prompt.sh.j2
│   ├── zsh/prompt.sh.j2
│   └── fish/prompt.sh.j2
│
├── tests/
│   ├── unit/                    # Unit tests
│   ├── integration/             # Integration tests
│   └── fixtures/                # Test fixtures
│
├── docs/                        # Documentation
├── scripts/                     # Build scripts
│
├── pyproject.toml               # Project config
├── README.md                    # This file
├── CHANGELOG.md                 # Version history
├── CONTRIBUTING.md              # Contribution guide
└── LICENSE                      # MIT License
```

---

## 🔧 Development

### Prerequisites

- Python 3.11 or higher
- pip
- git

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/trustlabs/clicool.git
cd clicool

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS

# Install with dev dependencies
pip install -e ".[dev]"

# Verify installation
clicool --version
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=clicool --cov-report=html

# Run specific test file
pytest tests/unit/test_theme_loader.py -v

# Run integration tests
pytest tests/integration/ -v
```

### Code Quality

```bash
# Check code style
ruff check clicool

# Format code
black clicool

# Type checking
mypy clicool

# Run all checks
ruff check clicool && black --check clicool && mypy clicool
```

### Building Package

```bash
# Install build tools
pip install build

# Build source and wheel
python -m build

# Install locally
pip install -e .

# Test installation
clicool doctor
```

### Creating Themes

```bash
# Validate theme
clicool theme validate my-theme.json

# Create new theme scaffold (coming soon)
clicool theme new my-theme
```

### Theme JSON Schema

Themes follow JSON Schema v2:

```json
{
  "$schema": "https://clicool.dev/schemas/theme-v2.json",
  "name": "My Theme",
  "version": "1.0.0",
  "prompt": {
    "format": "neon",
    "template": "{user}@{host}:{path} λ",
    "colors": { "user": "#00ffff" }
  },
  "features": { "show_git": true },
  "widgets": ["git", "time"]
}
```

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Ways to Contribute

- 🎨 **Create Themes** - Design new beautiful themes
- 🧅 **Build Layers** - Add new widget layers
- 🐛 **Fix Bugs** - Squash bugs in the codebase
- ✨ **Add Features** - Implement new features
- 📚 **Improve Docs** - Enhance documentation
- 🧪 **Write Tests** - Increase test coverage

### Getting Started

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Format code (`black .`)
6. Commit (`git commit -m 'Add amazing feature'`)
7. Push (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Write tests for new features
- Update documentation
- Add entry to CHANGELOG.md
- Use conventional commits

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📊 Performance

### Benchmarks

| Metric | Target | Actual |
|--------|--------|--------|
| Theme enable time | < 500ms | ~200ms |
| Prompt render time | < 50ms | ~25ms |
| Backup creation | < 200ms | ~100ms |
| Doctor check | < 1s | ~500ms |
| Memory usage | < 50MB | ~30MB |
| Install size | < 5MB | ~2MB |

*Tested on: Ubuntu 24.04, Python 3.12, Intel i7*

---

## 📝 Changelog

### [0.1.0] - 2026-03-03

**Added**
- Initial release with core functionality
- 5 built-in themes (Cyberpunk, Matrix, Retro, Minimal, DevOps)
- 4 layer themes (Git Status, K8s Context, Docker Info, AWS Profile)
- Shell support: Bash, Zsh, Fish
- Safety features: Auto-backup, rollback, dry-run
- Doctor command for diagnostics
- Widget system
- Banner animations
- Profile management (basic)
- 42 unit tests + 15 integration tests

See [CHANGELOG.md](CHANGELOG.md) for full version history.

---

## 🙏 Acknowledgments

CLICOOL is inspired by and builds upon the great work of:

- **[Starship](https://starship.rs/)** - Cross-shell prompt
- **[Oh My Zsh](https://ohmyz.sh/)** - Zsh framework
- **[Powerlevel10k](https://github.com/romkatv/powerlevel10k)** - Zsh theme
- **[Typer](https://typer.tiangolo.com/)** - CLI framework
- **[Rich](https://github.com/Textualize/rich)** - Terminal formatting

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

```
MIT License
Copyright (c) 2026 Trustlabs

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

---

## 🔗 Links

- **GitHub:** [github.com/trustlabs/clicool](https://github.com/trustlabs/clicool)
- **PyPI:** [pypi.org/project/clicool](https://pypi.org/project/clicool/)
- **Documentation:** [github.com/trustlabs/clicool#readme](https://github.com/trustlabs/clicool#readme)
- **Issues:** [github.com/trustlabs/clicool/issues](https://github.com/trustlabs/clicool/issues)
- **Discussions:** [github.com/trustlabs/clicool/discussions](https://github.com/trustlabs/clicool/discussions)

---

## 📬 Contact

- **Twitter:** [@trustlabs](https://twitter.com/trustlabs)
- **Discord:** [Join our server](https://discord.gg/clicool)
- **Email:** hello@clicool.dev

---

<div align="center">

### Ready to transform your terminal?

```bash
pip install clicool && clicool init && clicool enable cyberpunk
```

**Made with ⚡ by Trustlabs**

[Report Bug](https://github.com/trustlabs/clicool/issues) · [Request Feature](https://github.com/trustlabs/clicool/issues)

![Stars](https://img.shields.io/github/stars/trustlabs/clicool?style=social)
![Forks](https://img.shields.io/github/forks/trustlabs/clicool?style=social)

</div>
