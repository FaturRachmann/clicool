# CLICOOL Release Guide

## 📦 Publishing to PyPI

### Automated (Recommended)

CLICOOL uses GitHub Actions to automatically publish to PyPI when you create a version tag.

#### Steps to Release:

1. **Run the release script:**
   ```bash
   chmod +x scripts/release.sh
   ./scripts/release.sh
   ```

2. **Follow the prompts:**
   - Enter new version number (e.g., `0.1.0`)
   - Confirm the release

3. **The script will:**
   - Update version in `pyproject.toml`
   - Update `CHANGELOG.md`
   - Create git commit
   - Create git tag `v{version}`
   - Push to GitHub

4. **GitHub Actions will:**
   - Run tests
   - Build package
   - Publish to PyPI
   - Create GitHub Release

### Manual Release

If you prefer to release manually:

#### 1. Update Version

```bash
# Update version in pyproject.toml
# Update version in clicool/__init__.py
# Update CHANGELOG.md
```

#### 2. Build Package

```bash
# Install build tools
pip install build twine

# Build source and wheel
python -m build

# Check the built files
ls -la dist/
```

#### 3. Test Package Locally

```bash
# Install from local build
pip install dist/clicool-*.whl

# Test the CLI
clicool --version
clicool doctor
```

#### 4. Upload to TestPyPI (Optional but Recommended)

```bash
# Upload to TestPyPI first
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ clicool
```

#### 5. Upload to PyPI

```bash
# Upload to PyPI
twine upload dist/*

# You'll be prompted for credentials
# Use your PyPI API token
```

#### 6. Create GitHub Release

```bash
# Create and push tag
git tag v0.1.0
git push origin v0.1.0

# Create release on GitHub
# Go to: https://github.com/trustlabs/clicool/releases/new
# Select the tag
# Generate release notes
# Publish
```

---

## 🔑 Setup PyPI Credentials

### Get PyPI API Token

1. Go to https://pypi.org/manage/account/token/
2. Click "Add API token"
3. Give it a name (e.g., "clicool-github")
4. Set scope to "All projects" or specific project
5. Copy the token

### For GitHub Actions

1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `PYPI_API_TOKEN`
5. Value: Paste your PyPI token
6. Click "Add secret"

### For Manual Upload

Create `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-<your-pypi-token>

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-<your-testpypi-token>
```

---

## 📝 Version Numbering

CLICOOL uses [Semantic Versioning](https://semver.org/):

```
MAJOR.MINOR.PATCH
  │     │     │
  │     │     └─ Bug fixes (backward compatible)
  │     └─────── New features (backward compatible)
  └───────────── Breaking changes
```

Examples:
- `0.1.0` - Initial release
- `0.1.1` - Bug fix
- `0.2.0` - New features
- `1.0.0` - Stable release (breaking changes)

---

## 🧪 Testing Before Release

### 1. Run All Tests

```bash
pytest --cov=clicool
```

### 2. Check Code Quality

```bash
ruff check clicool
black --check clicool
mypy clicool --ignore-missing-imports
```

### 3. Build and Test Locally

```bash
# Build
python -m build

# Install locally
pip install -e .

# Test commands
clicool --version
clicool list
clicool doctor
clicool enable cyberpunk
```

### 4. Test Installation from Clean Environment

```bash
# Create fresh virtual environment
python -m venv test-env
source test-env/bin/activate

# Install from dist
pip install dist/clicool-*.whl

# Test
clicool --version
```

---

## 🚨 Troubleshooting

### Build Fails

```bash
# Clean build directory
rm -rf dist/ build/ *.egg-info

# Rebuild
python -m build
```

### Upload Fails (403 Forbidden)

- Check your API token is correct
- Ensure token has correct scope
- Check you're uploading to correct repository (pypi vs testpypi)

### Version Already Exists

- PyPI doesn't allow re-uploading same version
- Increment version number and try again

### Tests Fail on CI but Pass Locally

- Check Python version differences
- Check OS-specific paths
- Ensure all files are committed to git

---

## 📊 Release Checklist

Before releasing, ensure:

- [ ] All tests pass
- [ ] Code quality checks pass
- [ ] CHANGELOG.md is updated
- [ ] Version numbers updated
- [ ] Documentation is up to date
- [ ] No sensitive data in code
- [ ] All new files are in git
- [ ] README examples work

---

## 🔗 Useful Links

- [PyPI Documentation](https://packaging.python.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Semantic Versioning](https://semver.org/)
- [PyPI API Tokens](https://pypi.org/help/#apitoken)

---

<div align="center">

**Happy Releasing! 🚀**

</div>
