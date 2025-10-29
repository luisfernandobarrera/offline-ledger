# Troubleshooting Guide

## Common Issues and Solutions

### Issue 1: `uv sync` fails with build error

**Error:**
```
ValueError: Unable to determine which files to ship inside the wheel
```

**Solution:**
This was fixed in the `pyproject.toml` configuration. Make sure you have:
```toml
[tool.hatch.build.targets.wheel]
packages = ["app"]

[tool.hatch.build]
only-packages = true
```

If you still have issues, try:
```bash
rm -rf .venv uv.lock
uv sync
```

### Issue 2: Dashboard transaction amounts not showing

**Current Status:**
Transaction amounts in the dashboard currently show as "-". This is a temporary simplification while we properly implement JavaScript-based amount calculation.

**Workaround:**
- View detailed transaction amounts in the "Transactions" tab
- Click on any transaction to expand and see full debit/credit details
- The Reports section shows all financial totals correctly

**Why:**
Reflex's `rx.call_script()` returns an EventSpec that cannot be directly embedded in f-strings. The proper solution requires restructuring how amounts are calculated client-side.

### Issue 3: Wrong Python version

**Error:**
```
Python version mismatch or deprecation warning
```

**Solution:**
This project requires Python 3.13+ (3.13 recommended):
```bash
# Check your Python version
python --version

# If you need to install Python 3.13, use pyenv:
pyenv install 3.13.8
pyenv local 3.13.8

# Then reinstall with uv
rm -rf .venv uv.lock
uv sync
```

### Issue 4: Pydantic V1 warning with Python 3.14

**Warning:**
```
UserWarning: Core Pydantic V1 functionality isn't compatible with Python 3.14 or greater.
```

**Status:** ✅ **FIXED - Using Python 3.13**

This project now uses Python 3.13, which is fully compatible with Reflex and Pydantic V1. No more warnings!

**If you encounter this:**
Make sure you're using Python 3.13:
```bash
python --version  # Should show 3.13.x

# If not, reinstall:
echo "3.13" > .python-version
rm -rf .venv uv.lock
uv sync
```

### Issue 5: Sitemap plugin warning (FIXED)

**Warning:**
```
Warning: `reflex.plugins.sitemap.SitemapPlugin` plugin is enabled by default
```

**Status:** ✅ **FIXED**

This has been fixed in `rxconfig.py` by disabling the sitemap plugin (not needed for this app).

### Issue 6: state_auto_setters deprecation warnings (FIXED)

**Warning:**
```
DeprecationWarning: state_auto_setters defaulting to True has been deprecated
```

**Status:** ✅ **FIXED**

All explicit setters have been added to `app/state.py`. The app no longer relies on auto-generated setters.

### Issue 7: App won't start after changes

**Solution:**
Clear the cache and rebuild:
```bash
rm -rf .web .states
uv run reflex init
uv run reflex run
```

### Issue 8: Dependencies out of sync

**Solution:**
Reinstall all dependencies:
```bash
rm -rf .venv uv.lock
uv sync
```

### Issue 9: Port already in use

**Error:**
```
Address already in use
```

**Solution:**
```bash
# Find and kill the process using port 3000
lsof -ti:3000 | xargs kill -9

# Or use a different port
uv run reflex run --loglevel debug --port 3001
```

## Getting Help

If you encounter issues not listed here:

1. **Check the logs**: Look for error messages in the terminal
2. **Clear cache**: `rm -rf .web .states && uv run reflex init`
3. **Reinstall**: `rm -rf .venv uv.lock && uv sync`
4. **Check documentation**: See [Reflex docs](https://reflex.dev/docs/)

## Known Limitations

### Transaction Amount Display
- Dashboard transaction list shows "-" instead of amounts
- This is a known limitation of the current Reflex version
- Full transaction details are available in the Transactions tab
- All financial reports calculate amounts correctly

### Dark Mode
- Dark mode toggle updates the theme
- Some components may need page refresh to fully apply theme
- LocalStorage saves your preference automatically

## Development Tips

### Fast Refresh
If the app doesn't reflect your changes:
```bash
# Ctrl+C to stop the server, then:
uv run reflex run
```

### Debug Mode
For more detailed error messages:
```bash
uv run reflex run --loglevel debug
```

### Production Build
To test production mode:
```bash
uv run reflex run --env prod
```

## Performance

### Slow Startup
First startup is always slower as Reflex:
- Installs Node.js dependencies
- Compiles the frontend
- Generates static assets

Subsequent starts are much faster.

### Memory Usage
If the app uses too much memory:
- Close unused browser tabs
- Clear browser LocalStorage if data is very large
- Export and reimport data periodically

## Data Safety

### Backup Regularly
Your data is in browser LocalStorage. To avoid loss:
1. Export data regularly (Settings → Export)
2. Keep backups in multiple locations
3. Test imports occasionally

### Browser Cache
Clearing browser cache won't delete your data, but:
- Don't clear "LocalStorage"
- Export before major browser updates
- Test in private/incognito first

---

**Last Updated:** October 28, 2025
**Reflex Version:** 0.8.17+
**Python Version:** 3.13+ (3.13 recommended)

