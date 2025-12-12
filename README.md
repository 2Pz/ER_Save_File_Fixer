# Elden Ring Torrent State Fixer

Fixes the infinite loading screen bug caused by Torrent being stuck in an active state with 0 HP.

## What's the problem?

When you die on Torrent and instantly crash/alt + f4 the state of Torrent might not get updated but will still be set to Active. This causes an infinite loading screen.

## What does this do?

Scans your save file and fixes Torrent's state so the game can load normally. Creates a backup automatically.

## Download

[Get the latest exe here](../../releases/latest)

## Usage

1. Close Elden Ring
2. Run the exe
3. Click "Auto-Find" or browse to your save manually
4. Click "Fix Torrent State"

Works with standard saves (.sl2) and Seamless Co-op saves (.co2).

## Running from source

```bash
python elden_ring_torrent_fixer.py
```

Requires Python 3.6+ with tkinter.

## Building

```bash
pip install pyinstaller
pyinstaller elden_ring_torrent_fixer.spec
```

## Note

Backups are created automatically but use at your own risk.
