# Quick Start Guide - Offline Ledger

This is a fast reference for getting started with the Offline Ledger application using `uv`.

## 🚀 First Time Setup

### 1. Install uv (one time only)

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Install Dependencies

```bash
cd offline-ledger
uv sync
```

### 3. Initialize Reflex (first time only)

```bash
uv run reflex init
```

### 4. Run the App

```bash
uv run reflex run
```

Open http://localhost:3000 in your browser 🎉

---

## 📝 Daily Usage

```bash
# Start the development server
uv run reflex run

# That's it! Just this one command for daily use.
```

---

## 🛠️ Common Commands

```bash
# Add a new Python package
uv add package-name

# Remove a package
uv remove package-name

# Update all dependencies
uv sync --upgrade

# Run in production mode
uv run reflex run --env prod

# Export as static site
uv run reflex export

# Clear Reflex cache (if you have issues)
uv run reflex init --reset
```

---

## 🎯 Keyboard Shortcuts

- `Ctrl/Cmd + N` - New Account
- `Ctrl/Cmd + Shift + N` - New Transaction
- `Ctrl/Cmd + D` - Dashboard
- `Ctrl/Cmd + ,` - Settings

---

## 💾 Data Management

Your data is automatically saved in your browser's LocalStorage.

**To backup your data:**
1. Click Settings (gear icon)
2. Click "Export" under Data Management
3. Save the JSON file somewhere safe

**To restore data:**
1. Click Settings
2. Click "Import" under Data Management
3. Select your backup JSON file

---

## 🌐 Multi-Language Support

Click the language dropdown in the header to switch between:
- 🇬🇧 English
- 🇪🇸 Spanish
- 🇫🇷 French
- 🇨🇳 Chinese
- 🇵🇹 Portuguese

---

## 🌙 Dark Mode

Click the moon/sun icon in the header to toggle dark mode.

---

## 🐍 Python Version

This project requires **Python 3.13+**. Check your version:
```bash
python --version
# Should show Python 3.13.x
```

**Why 3.13?** Python 3.13 provides the best compatibility with Reflex and all its dependencies (including Pydantic V1).

## ❓ Troubleshooting

**App won't start?**
```bash
# Clear cache and reinitialize
uv run reflex init --reset
uv run reflex run
```

**Dependencies issue?**
```bash
# Reinstall dependencies
rm -rf .venv uv.lock
uv sync
```

**Need to reset everything?**
```bash
# Clear all Reflex generated files
rm -rf .web .states
uv run reflex init
```

---

## 📚 More Information

See `README.md` for complete documentation including:
- Detailed feature list
- Accounting principles
- Technical architecture
- Development guidelines

---

**Tip:** Keep this file bookmarked for quick reference! 📌

