# Auto-Run Setup for VoiceCraft

This guide explains how to enable automatic scanning and disable confirmation prompts.

## Quick Setup

### Enable Auto-Scan

The auto-scan feature is **already enabled** by default. The `.voicecraft_auto` config file has been created with:

```
AUTO_SCAN=1
AUTO_YES=1
AUTO_UPDATE=1
```

### Manual Run

To manually run the scan:
```bash
python3 auto_scan.py
```

To force run even if disabled:
```bash
python3 auto_scan.py --force
```

## Auto-Run Features

### 1. Git Hook (Post-Commit)

The scan automatically runs after each git commit. The hook is located at:
```
.git/hooks/post-commit
```

**To disable:** Remove or rename the hook file, or set `AUTO_SCAN=0` in `.voicecraft_auto`

### 2. Skip Confirmation Prompts

Set the `AUTO_YES` environment variable or use the `--yes` flag:

```bash
# Environment variable (persistent)
export AUTO_YES=1

# Or per command
voicecraft --yes profile create --name "Name" --samples "./*.md"
```

### 3. Environment Variables

You can control auto-run behavior with environment variables:

```bash
# Enable auto-scan
export AUTO_SCAN=1

# Skip all prompts
export AUTO_YES=1

# Auto-update on file changes (future feature)
export AUTO_UPDATE=1
```

## Configuration File

The `.voicecraft_auto` file controls auto-run behavior:

```bash
# Enable/disable auto-scan
AUTO_SCAN=1  # or 0 to disable

# Skip confirmation prompts
AUTO_YES=1   # or 0 to show prompts

# Auto-update summary (future)
AUTO_UPDATE=1  # or 0 to disable
```

## Disabling Auto-Run

### Disable Git Hook
```bash
# Remove the hook
rm .git/hooks/post-commit

# Or disable in config
echo "AUTO_SCAN=0" > .voicecraft_auto
```

### Disable Environment Variable
```bash
unset AUTO_SCAN
unset AUTO_YES
```

## Troubleshooting

### Git Hook Not Running

1. Check if hook exists:
   ```bash
   ls -la .git/hooks/post-commit
   ```

2. Make sure it's executable:
   ```bash
   chmod +x .git/hooks/post-commit
   ```

3. Check git config:
   ```bash
   git config core.hooksPath .git/hooks
   ```

### Auto-Scan Not Working

1. Check config file:
   ```bash
   cat .voicecraft_auto
   ```

2. Check environment variables:
   ```bash
   echo $AUTO_SCAN
   ```

3. Test manual run:
   ```bash
   python3 auto_scan.py --force
   ```

## Current Status

✅ **Auto-scan script:** Created (`auto_scan.py`)  
✅ **Git hook:** Created (`.git/hooks/post-commit`)  
✅ **Config file:** Created (`.voicecraft_auto`)  
✅ **CLI --yes flag:** Added to main CLI group  
✅ **Environment variables:** Supported

**Everything is set up and ready to auto-run!** 🚀

