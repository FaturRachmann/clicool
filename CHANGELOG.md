# Changelog

All notable changes to clicool will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-03-03

### Added
- Initial project structure
- CLI entry point with Typer
- Shell detection (bash, zsh, fish)
- Terminal emulator detection
- Theme JSON loader with Pydantic validation
- Config injection system with markers
- Backup and restore functionality
- Rollback engine
- Config diff viewer
- Doctor command for diagnostics
- Theme preview functionality
- Layer system for modular themes
- Widget system (git, time, k8s, docker, aws)
- Banner animations (typewriter, fade-in, glitch, matrix)
- 5 built-in themes:
  - Cyberpunk
  - Matrix
  - Retro
  - Minimal
  - DevOps
- 4 layer themes:
  - Git Status
  - Kubernetes Context
  - Docker Info
  - AWS Profile
- Shell templates for bash, zsh, fish
- Color utilities and converters
- Font detection utilities
- Template engine with Jinja2
- Logging utilities

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- N/A

---

## [0.1.0] - 2026-03-03

### Added
- Initial release
- MVP with core theme management functionality
- Basic CLI commands: enable, disable, list, preview, doctor, backup, restore
- Safety features: automatic backups, marker-based injection
- Cross-shell support for bash and zsh
- Comprehensive documentation

---

[Unreleased]: https://github.com/trustlabs/clicool/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/trustlabs/clicool/releases/tag/v0.1.0
