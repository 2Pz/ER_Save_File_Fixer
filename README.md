# Elden Ring Save File Fixer

Fixes infinite loading screen issues caused by Torrent bugs and DLC location problems.

## What does this fix?

**Torrent Stuck Loading Bug**
When you die on Torrent and crash/alt+F4, Torrent can get stuck in an "Active" state with 0 HP, causing infinite loading screens.

**DLC Location Bug**
If you're stuck in a DLC location without the DLC, the game won't load. This teleports you back to Limgrave.

## Download

[Get the latest release here](../../releases/latest)

## How to Use

1. Close Elden Ring completely
2. Run the application
3. Click "Auto-Find" or "Browse" to select your save file
4. Click "Load Characters"
5. Select the stuck character from the list
6. Click "Fix Selected Character"

The tool will create an automatic backup, detect any issues, and apply the necessary fixes.

## Compatibility

- Standard saves (.sl2)
- Seamless Co-op saves (.co2)
- All 10 character slots

## Running from Source

Requires Python 3.7+ with tkinter:
```bash
python elden_ring_save_fixer_gui.py
```

## Building
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "Elden Ring Save Fixer" elden_ring_save_fixer_gui.py
```

## Safety

Automatic backups are created before any changes. Use the "Restore Backup" button if something goes wrong.

## Credits

Save file parsing based on [ClayAmore's Elden Ring Save Templates](https://github.com/ClayAmore/EldenRingSaveTemplate)