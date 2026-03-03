#!/bin/bash
# Release script for CLICOOL
# This script helps you create a new release and publish to PyPI

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    log_error "Please run this script from the project root directory"
    exit 1
fi

# Get current version
CURRENT_VERSION=$(grep -m1 "^version = " pyproject.toml | cut -d'"' -f2)
log_info "Current version: ${CURRENT_VERSION}"

# Prompt for new version
echo ""
echo "Enter new version number (current: ${CURRENT_VERSION}):"
read -p "v" NEW_VERSION

if [ -z "$NEW_VERSION" ]; then
    log_error "Version number cannot be empty"
    exit 1
fi

# Validate version format
if [[ ! "$NEW_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    log_error "Invalid version format. Please use semantic versioning (e.g., 0.1.0)"
    exit 1
fi

log_info "New version: ${NEW_VERSION}"

# Confirm
echo ""
log_warn "This will:"
echo "  1. Update version in pyproject.toml to ${NEW_VERSION}"
echo "  2. Update CHANGELOG.md"
echo "  3. Create git commit"
echo "  4. Create git tag v${NEW_VERSION}"
echo "  5. Push to GitHub (which will trigger PyPI publish)"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    log_info "Aborted"
    exit 0
fi

# Update version in pyproject.toml
log_info "Updating version in pyproject.toml..."
sed -i "s/^version = \"${CURRENT_VERSION}\"/version = \"${NEW_VERSION}\"/" pyproject.toml

# Update CHANGELOG.md
log_info "Updating CHANGELOG.md..."
if grep -q "## \[Unreleased\]" CHANGELOG.md; then
    # Replace Unreleased with new version and date
    sed -i "s/## \[Unreleased\]/## [${NEW_VERSION}] - $(date +%Y-%m-%d)/" CHANGELOG.md
    
    # Add new Unreleased section at top
    sed -i '1,/^## /{
        /^## /i\
## [Unreleased]\
\
### Added\
- N/A\
\
### Changed\
- N/A\
\
### Deprecated\
- N/A\
\
### Removed\
- N/A\
\
### Fixed\
- N/A\
\
### Security\
- N/A\
\
}
    ' CHANGELOG.md
fi

# Update __init__.py version
if [ -f "clicool/__init__.py" ]; then
    log_info "Updating version in __init__.py..."
    sed -i "s/^__version__ = \".*\"/__version__ = \"${NEW_VERSION}\"/" clicool/__init__.py
fi

# Git operations
log_info "Creating git commit..."
git add pyproject.toml CHANGELOG.md clicool/__init__.py
git commit -m "chore: release version ${NEW_VERSION}" || log_warn "No changes to commit"

log_info "Creating git tag v${NEW_VERSION}..."
git tag "v${NEW_VERSION}"

log_info "Pushing to GitHub..."

# Check if using HTTPS remote
REMOTE_URL=$(git remote get-url origin)
if [[ $REMOTE_URL == https://* ]]; then
    log_warn "Using HTTPS remote. SSH is recommended for easier authentication."
    log_info "To switch to SSH, run:"
    log_info "  git remote set-url origin git@github.com:FaturRachmann/clicool.git"
    echo ""
fi

git push origin main
git push origin "v${NEW_VERSION}"

log_info "✓ Release v${NEW_VERSION} created successfully!"
echo ""
log_warn "GitHub Actions will now build and publish to PyPI."
log_info "Monitor the workflow at: https://github.com/trustlabs/clicool/actions"
echo ""
log_info "Once published, the package will be available at:"
log_info "https://pypi.org/project/clicool/${NEW_VERSION}/"
