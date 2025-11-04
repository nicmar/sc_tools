# 🚀 Time Travel in Space Chef: How to Restore Your Save Files

## Hit a nasty bug? Want to undo that catastrophic decision? Need to go back in time?

Good news! Space Chef automatically creates a **backup of your save file every day**, so you can always rewind time and try again. Whether you encountered a game-breaking bug, made a terrible choice, or just want to replay a favorite moment, your past saves are waiting for you.

## 🎮 The Quick & Easy Way: Space Chef Save Manager

We've created a free tool that makes managing your saves super simple:

**[⬇️ Download Space Chef Save Manager for Windows](https://github.com/nicmar/sc_tools/releases/latest/download/SpaceChefSaveManager-v1.0.1-Windows.zip)**

- ✨ See all your saves with player names and day numbers
- 📅 View all available backups sorted by date
- ⚡ One-click restore (with automatic safety backup)
- 🖱️ No installation needed - just extract and run!
- 🌍 Also available for [macOS](https://github.com/nicmar/sc_tools/releases/latest) and [Linux](https://github.com/nicmar/sc_tools/releases/latest)

> **Note:** Windows may show a SmartScreen warning (the app isn't signed). Just click "More info" → "Run anyway" - it's safe!

### Using the Tool

1. Extract the ZIP and run `SpaceChefSaveManager.exe`
2. Select your player/save file
3. Click **"View Backups"** to see all your time-travel points
4. Pick a backup and click **"Restore Selected"**
5. Confirm and you're done! ✨

**Pro tip:** The tool is [open source on GitHub](https://github.com/nicmar/sc_tools) if you want to check the code or build it yourself!

---

## 🛠️ The Manual Way: DIY Restoration

Prefer to do it yourself? No problem! Here's where Space Chef hides your backups:

### Find Your Saves Folder

**Windows:**
```
C:\Users\<YourName>\AppData\LocalLow\BlueGooGames\Space Chef\Saves
```
*(Tip: Copy-paste this into File Explorer's address bar, replacing `<YourName>` with your username)*

**Other platforms:** See the [full guide here](https://github.com/nicmar/sc_tools/blob/main/space-chef-save-manager/README.md#default-save-locations)

### Restore a Backup Manually

1. **Close Space Chef completely**
2. Navigate to your `Saves` folder
3. Go into the `Backup` subfolder
4. Find the backup you want (they're named with dates like `save0001_2024-11-04_14-30-15.zip`)
5. **IMPORTANT:** Copy your current save somewhere safe first (just in case!)
   - Copy `save0001.json` to your desktop
6. Extract the backup ZIP file
7. Copy the `.json` file from the backup and replace your current save file
8. Launch Space Chef - you've time traveled! ⏰

---

## 📝 Understanding Your Backups

- **Automatic daily backups:** The game creates these every day you play
- **Backup naming:** `save####_YYYY-MM-DD_HH-MM-SS.zip`
- **Location:** Inside your `Saves/Backup/` folder
- **Multiple saves:** Each save slot (save0001, save0002, etc.) has its own backups

---

## ⚠️ Troubleshooting

**Can't find your Saves folder?**
- Make sure you've launched Space Chef at least once
- Check if the game installed in a non-standard location
- Use the Save Manager tool's "Browse" button to find it automatically

**Backup restore didn't work?**
- Make sure Space Chef is completely closed
- Check you have write permissions to the Saves folder
- Verify the backup file isn't corrupted (the ZIP should extract without errors)

**No backups available?**
- The game only creates backups when you play
- Very new saves might not have backups yet
- Check the `Backup` subfolder exists

---

## 🎉 Happy Time Traveling!

Now you can experiment, take risks, and explore without fear. Made a mistake? Just rewind and try again!

**Questions or issues?** Check out the [Space Chef Save Manager GitHub](https://github.com/nicmar/sc_tools) or leave a comment below.

---

*This is an unofficial community tool - not affiliated with BlueGoo Games, but made with ❤️ for Space Chef players!*
