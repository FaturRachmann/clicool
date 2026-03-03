# CLICOOL Usage Guide

## 🚀 Cara Menggunakan CLICOOL

### Quick Start (5 Menit)

```bash
# 1. Install
pip install clicool

# 2. Initialize
clicool init

# 3. Lihat tema yang tersedia
clicool list

# 4. Preview tema
clicool preview cyberpunk

# 5. Enable tema
clicool enable cyberpunk

# 6. Reload shell
source ~/.bashrc  # atau ~/.zshrc

# Done! Terminal Anda sekarang lebih cool! 🎉
```

---

## 📋 Command Lengkap

### Theme Commands

| Command | Deskripsi |
|---------|-----------|
| `clicool enable <theme>` | Enable tema |
| `clicool enable --random` | Random tema |
| `clicool enable <theme> -p` | Preview dulu |
| `clicool enable <theme> -n` | Dry run (lihat perubahan) |
| `clicool disable` | Disable tema |
| `clicool list` | List tema |
| `clicool preview <theme>` | Preview tema |
| `clicool demo` | Demo color palettes |

### Layer Commands

```bash
# Enable dengan layer
clicool enable cyberpunk --layer git-status
clicool enable devops --layer git-status --layer k8s-context
```

### Safety Commands

```bash
clicool doctor          # Check environment
clicool backup          # Create backup
clicool backup --list   # List backups
clicool restore         # Restore backup
clicool diff            # Lihat perubahan
clicool status          # Status tema aktif
```

---

## 🎨 Daftar Tema

### 1. Cyberpunk
**Neon-soaked futuristic**

```bash
clicool enable cyberpunk
```

**Warna:** Cyan, Magenta, Yellow
**Cocok untuk:** Night coding, cyberpunk aesthetic

### 2. Matrix
**Classic hacker green**

```bash
clicool enable matrix
```

**Warna:** Green on black
**Cocok untuk:** Hacker aesthetic

### 3. Retro
**Amber CRT monitor vibes**

```bash
clicool enable retro
```

**Warna:** Amber on dark
**Cocok untuk:** Vintage lovers

### 4. Minimal
**Clean and subtle**

```bash
clicool enable minimal
```

**Warna:** Grayscale dengan blue accents
**Cocok untuk:** Professional settings

### 5. DevOps
**For SREs and Platform Engineers**

```bash
clicool enable devops
```

**Warna:** Blue, green, purple
**Widgets:** Git, K8s, Docker, AWS
**Cocok untuk:** DevOps, SRE, cloud engineers

---

## 🧅 Layer System

Layers menambahkan informasi real-time ke prompt Anda.

### Available Layers

| Layer | Fungsi | Contoh Output |
|-------|--------|---------------|
| `git-status` | Git branch + status | `(main) ✗` |
| `k8s-context` | Kubernetes context | `☸️ prod/us-east` |
| `docker-info` | Container count | `🐳 5` |
| `aws-profile` | AWS profile | `☁️ prod@us-east-1` |

### Cara Pakai Layers

```bash
# Single layer
clicool enable cyberpunk --layer git-status

# Multiple layers
clicool enable devops \
  --layer git-status \
  --layer k8s-context \
  --layer docker-info
```

---

## 💡 Tips & Tricks

### 1. Preview Dulu Sebelum Enable

```bash
# Lihat preview dengan warna
clicool preview cyberpunk

# Lihat demo semua tema
clicool demo
```

### 2. Dry Run Mode

```bash
# Lihat apa yang akan berubah
clicool enable cyberpunk --dry-run
```

### 3. Backup Manual

```bash
# Create backup sebelum enable
clicool backup

# List backups
clicool backup --list
```

### 4. Check Environment

```bash
# Check jika ada masalah
clicool doctor

# Verbose mode
clicool doctor --verbose
```

### 5. Lihat Perubahan

```bash
# Lihat apa yang berubah di config
clicool diff
```

---

## 🔧 Troubleshooting

### Tema Tidak Muncul Perubahan

**Problem:** Setelah enable, prompt tidak berubah.

**Solution:**

```bash
# 1. Pastikan tema ter-enject
grep "CLICOOL" ~/.bashrc

# 2. Reload shell
source ~/.bashrc

# 3. Restart terminal jika perlu
```

### Warna Tidak Keluar

**Problem:** Prompt muncul tapi tanpa warna.

**Solution:**

```bash
# 1. Check jika terminal support color
echo $COLORTERM

# Harus: truecolor atau 24bit

# 2. Update terminal emulator
# Gunakan: GNOME Terminal, Kitty, Alacritty, iTerm2
```

### Git Branch Tidak Muncul

**Problem:** Git branch tidak muncul di prompt.

**Solution:**

```bash
# 1. Check jika git terinstall
git --version

# 2. Enable dengan layer git-status
clicool enable cyberpunk --layer git-status
```

### Error Saat Enable

**Problem:** Error saat enable tema.

**Solution:**

```bash
# 1. Check environment
clicool doctor

# 2. Enable dengan dry-run dulu
clicool enable cyberpunk --dry-run

# 3. Restore backup jika ada masalah
clicool restore --list
clicool restore <backup_id>
```

---

## 📊 Performance

CLICOOL didesain untuk minimal impact:

| Metric | Target | Actual |
|--------|--------|--------|
| Prompt render | <50ms | ~25ms |
| Theme enable | <500ms | ~200ms |
| Memory usage | <50MB | ~30MB |

---

## 🎯 Next Steps

Setelah install dan enable tema:

1. **Explore layers** - Tambahkan widget yang berguna
2. **Customize** - Edit `~/.clicool/config.json`
3. **Share** - Screenshot terminal Anda!
4. **Contribute** - Buat tema sendiri!

---

## 📚 Resources

- [GitHub](https://github.com/trustlabs/clicool)
- [Documentation](https://github.com/trustlabs/clicool#readme)
- [Issues](https://github.com/trustlabs/clicool/issues)
- [Discord](https://discord.gg/clicool)

---

<div align="center">

**Happy Customizing! 🎨**

</div>
