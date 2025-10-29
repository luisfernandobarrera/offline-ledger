# Migration to uv - Summary

This document summarizes the changes made to migrate the offline-ledger project to use `uv` as the package manager.

## 📋 Changes Made

### 1. New Files Created

#### `pyproject.toml`
- Modern Python project configuration file
- Defines project metadata (name, version, description)
- Specifies dependencies (`reflex>=0.8.15a1`)
- Configures build system (hatchling)
- Specifies package location (`app` directory)
- Includes optional dev dependencies (ruff for linting)
- Configures ruff linter settings

#### `.python-version`
- Specifies Python 3.10 as the required version
- Used by uv to ensure correct Python version

#### `QUICK_START.md`
- Concise quick reference guide
- Step-by-step setup instructions
- Common commands reference
- Keyboard shortcuts
- Data management tips
- Troubleshooting section

#### `MIGRATION_TO_UV.md`
- This file - documents the migration process

### 2. Files Updated

#### `README.md`
- Added "Quick Start" section with one-line setup command
- Added "Why uv?" explanation section
- Expanded installation instructions with uv commands
- Added new "Development Commands" section with uv examples
- Updated project structure to show new files
- Added uv to the technologies list
- Updated acknowledgments to mention uv
- Added "Tips" section with performance and data safety notes
- Changed tagline to "Made with ❤️ using Reflex + uv"

#### `.gitignore`
- Added uv-specific ignores (`.venv/`, `uv.lock`)
- Added comprehensive Python ignores
- Added IDE-specific ignores (`.vscode/`, `.idea/`)
- Added OS-specific ignores (`.DS_Store`, `Thumbs.db`)

### 3. Files Kept (Backward Compatibility)

#### `requirements.txt`
- Kept for users who prefer pip
- Noted as "legacy" in documentation
- Users can still use: `pip install -r requirements.txt`

## 🎯 Benefits of uv

1. **Speed**: 10-100x faster than pip
2. **Automatic Virtual Environments**: No need to manually create/activate venvs
3. **Reproducible Builds**: Lock file ensures consistent installations
4. **Better Dependency Resolution**: Faster and more reliable than pip
5. **Modern Tooling**: Built with Rust for performance

## 🚀 Migration Guide for Users

### If you were using pip before:

```bash
# Old way
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
reflex run

# New way (much simpler!)
uv sync
uv run reflex run
```

### Key Differences

| Aspect | pip | uv |
|--------|-----|-----|
| Virtual env | Manual creation | Automatic |
| Install speed | Slower | 10-100x faster |
| Configuration | `requirements.txt` | `pyproject.toml` |
| Lock file | None (or pip-tools) | `uv.lock` (automatic) |
| Running commands | Need to activate venv | `uv run <command>` |

## 📝 Commands Comparison

| Task | pip | uv |
|------|-----|-----|
| Install deps | `pip install -r requirements.txt` | `uv sync` |
| Add package | `pip install package-name` | `uv add package-name` |
| Remove package | `pip uninstall package-name` | `uv remove package-name` |
| Run app | `reflex run` | `uv run reflex run` |
| Update all | `pip install -U -r requirements.txt` | `uv sync --upgrade` |

## 🔄 What Happens Under the Hood

1. **`uv sync`**:
   - Reads `pyproject.toml`
   - Creates a virtual environment in `.venv/` (if it doesn't exist)
   - Installs all dependencies
   - Creates/updates `uv.lock` file for reproducibility

2. **`uv run`**:
   - Automatically activates the virtual environment
   - Runs the specified command
   - Deactivates when done

3. **Lock File (`uv.lock`)**:
   - Automatically created/updated
   - Ensures everyone gets the exact same dependency versions
   - Should be committed to git

## 🛠️ Troubleshooting

### Issue: "Command not found: uv"
**Solution**: Install uv first
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Issue: Dependencies not installing
**Solution**: Clear cache and resync
```bash
rm -rf .venv uv.lock
uv sync
```

### Issue: Want to use pip instead
**Solution**: No problem! Just use requirements.txt
```bash
pip install -r requirements.txt
reflex run
```

## 📚 Resources

- [uv Documentation](https://docs.astral.sh/uv/)
- [Python Packaging Guide](https://packaging.python.org/)
- [pyproject.toml Specification](https://peps.python.org/pep-0621/)

## ✅ Verification

To verify the migration was successful:

```bash
# Check uv is installed
uv --version

# Sync dependencies
cd offline-ledger
uv sync

# Run the app
uv run reflex run
```

If the app starts and you can access it at http://localhost:3000, the migration is complete! 🎉

---

**Migration completed on**: October 28, 2025
**uv version**: Check with `uv --version`
**Python version**: 3.13+ (3.13.8 recommended for best compatibility)

