# GitHub Authentication Setup

## Problem
Authentication failed saat push ke GitHub menggunakan HTTPS.

## Solutions

### Option 1: Use SSH (Recommended)

#### 1. Generate SSH Key

```bash
# Check if you already have SSH key
ls -la ~/.ssh

# Generate new SSH key (if needed)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Or use RSA (older systems)
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

#### 2. Add SSH Key to GitHub

```bash
# Copy your public key
cat ~/.ssh/id_ed25519.pub

# Or
cat ~/.ssh/id_rsa.pub
```

Then:
1. Go to https://github.com/settings/keys
2. Click "New SSH key"
3. Paste your public key
4. Click "Add SSH key"

#### 3. Change Remote to SSH

```bash
# Check current remote
git remote -v

# Change to SSH
git remote set-url origin git@github.com:FaturRachmann/clicool.git

# Verify
git remote -v
# Should show: git@github.com:FaturRachmann/clicool.git
```

#### 4. Test Connection

```bash
ssh -T git@github.com
# Should see: Hi FaturRachmann! You've successfully authenticated...
```

#### 5. Push Again

```bash
# Now push should work
git push origin main
git push origin v0.1.2
```

---

### Option 2: Use Personal Access Token (PAT)

#### 1. Create Personal Access Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Give it a name: `clicool-push`
4. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
5. Click "Generate token"
6. **Copy the token** (you won't see it again!)

#### 2. Use Token for Push

```bash
# When prompted for password, use your token instead
Username for 'https://github.com': FaturRachmann
Password for 'https://github.com': [paste your token here]
```

#### 3. Or Cache Credentials

```bash
# Cache credentials for 1 hour
git config --global credential.helper cache

# Or cache permanently
git config --global credential.helper store

# Then push again
git push origin main
```

---

### Option 3: Use GitHub CLI

#### 1. Install GitHub CLI

```bash
# Ubuntu/Debian
sudo apt install gh

# Or see: https://github.com/cli/cli#installation
```

#### 2. Authenticate

```bash
gh auth login
# Follow the prompts
```

#### 3. Push

```bash
git push origin main
```

---

## Quick Fix for Current Situation

Since you already created the commit and tag, just need to push:

### Method A: Using SSH (If already set up)

```bash
# Change remote to SSH
git remote set-url origin git@github.com:FaturRachmann/clicool.git

# Push
git push origin main
git push origin v0.1.2
```

### Method B: Using PAT

```bash
# Push with token in URL (replace YOUR_TOKEN with actual token)
git push https://FaturRachmann:YOUR_TOKEN@github.com/FaturRachmann/clicool.git main
git push https://FaturRachmann:YOUR_TOKEN@github.com/FaturRachmann/clicool.git v0.1.2
```

### Method C: Store Credentials

```bash
# Enable credential helper
git config --global credential.helper store

# Push (will prompt for credentials once, then remember)
git push origin main
```

---

## Verify Push

After pushing, verify:

```bash
# Check tags on remote
git ls-remote --tags origin

# Check branches
git ls-remote --heads origin
```

## Update Release Script

To make future releases easier, update the release script to use SSH by default:

Edit `scripts/release.sh`:

```bash
# Add this at the beginning
# Check if remote is HTTPS and suggest SSH
REMOTE_URL=$(git remote get-url origin)
if [[ $REMOTE_URL == https://* ]]; then
    echo -e "\033[1;33m[WARN]\033[0m Using HTTPS remote. Consider switching to SSH for easier authentication."
    echo "Run: git remote set-url origin git@github.com:FaturRachmann/clicool.git"
fi
```

---

## Recommended Setup

For best experience:

1. **Use SSH** for git operations
2. **Use PAT** for GitHub Actions (already set up with secrets)
3. **Enable credential helper** for occasional HTTPS operations

```bash
# Setup SSH
git remote set-url origin git@github.com:FaturRachmann/clicool.git

# Enable credential helper
git config --global credential.helper cache

# Test
git push origin main
```

---

<div align="center">

**Happy Pushing! 🚀**

</div>
