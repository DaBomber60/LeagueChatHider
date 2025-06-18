# LeagueChatHider

[![Latest Release](https://img.shields.io/github/v/release/DaBomber60/LeagueChatHider?style=flat-square)](https://github.com/DaBomber60/LeagueChatHider/releases/latest)

LeagueChatHider is a lightweight Windows tray application that automatically mutes in-game chat in *League of Legends* as soon as the game starts. It monitors the Riot client API, updates necessary config offsets, and runs a macro to disable chat. All interactions live in the system tray for a seamless experience.

---

## Features

- **Auto-Detection**: Waits for the League client and loading screen to finish before muting chat.
- **Config Patching**: Ensures `NativeOffsetX`/`NativeOffsetY` are set in both `game.cfg` and `PersistedSettings.json`.
- **Macro Mute**: Runs a PyAutoGUI/PyDirectInput macro to `/mute all` players.
- **Tray UI**: Displays current state, version, and quick links (GitHub repo, Exit).
- **Flexible Path**: On first run, lets you select a custom League install directory and saves it to `settings.ini`.

## Prerequisites

- **OS**: Windows 10 or later
- **Python**: 3.8+

Install dependencies:
```powershell
pip install -r requirements.txt
```

## Running from Source

```powershell
cd D:\Code\LeagueChatHider
python __main__.py
```

## Building a Standalone Executable

1. Install [PyInstaller](https://pyinstaller.org) and [UPX](https://upx.github.io/).
2. From your project root, run:
```powershell
pyinstaller __main__.spec --clean --noconfirm --upx-dir "C:\Program Files\upx"
```
3. The compact `.exe` will be available under `dist\LeagueChatHider\LeagueChatHider.exe`.

## Installation

Download the prebuilt executuable [from the releases page](https://github.com/DaBomber60/LeagueChatHider/releases/latest).

## Usage

- On first launch, if the default path (`C:\Riot Games\League of Legends`) is not found, you’ll be prompted to select the installation directory. This is saved to `settings.ini` next to the script.
- Use the tray icon menu to view current status, version number, open the GitHub repo, or exit.

## Configuration File

- **`settings.ini`**: Auto-generated in the script folder, stores your chosen `league_dir` path.

## Releases

Latest release: [https://github.com/DaBomber60/LeagueChatHider/releases/latest](https://github.com/DaBomber60/LeagueChatHider/releases/latest)

## License

This project is licensed under the [GPL-3.0 License](LICENSE).
