# Cursor Auto-Execute Setup

## Quick Fix: Add to Your Settings

### Option 1: Workspace Settings (Recommended)
I've created `.vscode/settings.json` in your VoiceCraft project with auto-execute settings.

### Option 2: Global Cursor Settings

1. **Open Cursor Settings:**
   - Press `Cmd+,` (or `Ctrl+,` on Windows)
   - Or: `Cmd+Shift+P` → "Preferences: Open User Settings (JSON)"

2. **Add these settings to your `settings.json`:**

```json
{
  "cursor.composer.autoExecute": true,
  "cursor.composer.skipConfirmation": true,
  "cursor.chat.autoExecute": true
}
```

### Option 3: Via Settings UI

1. Press `Cmd+,` to open Settings
2. Search for: `cursor composer`
3. Look for:
   - "Auto Execute"
   - "Skip Confirmation"
   - "Auto Approve"

## Settings to Try

If the above don't work, try these alternative setting names:

```json
{
  "composer.autoExecute": true,
  "composer.skipConfirmation": true,
  "cursor.planMode.autoExecute": true,
  "cursor.planMode.skipConfirmation": true,
  "cursor.automation.autoExecute": true
}
```

## Verify It's Working

After adding settings:
1. Reload Cursor: `Cmd+Shift+P` → "Developer: Reload Window"
2. Try creating a plan - it should execute automatically without asking

## If Still Not Working

1. **Check Cursor Version:** Some settings may be version-specific
2. **Check Command Palette:** `Cmd+Shift+P` → search for "composer" or "plan"
3. **Check Cursor Settings UI:** `Cmd+,` → search for "execute" or "confirmation"

## Location of Settings Files

- **User Settings:** `~/Library/Application Support/Cursor/User/settings.json`
- **Workspace Settings:** `.vscode/settings.json` (in your project)

---

**Note:** The exact setting names may vary by Cursor version. If these don't work, the feature might not be available yet or may be named differently.

