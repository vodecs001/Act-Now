# Act Now

Act Now is a lightweight Windows desktop sticky todo app for keeping daily tasks close at hand, especially near the screen edge.

## Features

- Todos: add, complete, delete, and archive tasks automatically when completed.
- Creation time: each todo shows its creation time in the lower-left corner.
- Groups: use All Todos or custom groups; deleting a group moves its todos to the default group.
- Archive: restore, delete individual completed todos, or clear the whole archive.
- Edge hide: supports left, right, and top edge hiding; the bottom edge does not trigger hiding.
- Top auto-hide: drag the window to the top of the screen to hide it, then move the pointer near the top edge to reveal it.
- Window controls: drag to move, drag to resize, minimize to the taskbar, or configure the close button to exit or minimize to tray.
- Startup: optional start with Windows.
- Languages: Chinese, English, and Japanese. The main UI and tray menu follow the selected language.
- Material You style: light surfaces, soft container colors, clear input field, and hover highlights on title-bar buttons.
- Taskbar and tray: the app appears in both the Windows taskbar and system tray.

## Install

Recommended installer:

```text
release\快办安装程序.exe
```

The installer lets you choose the installation folder and create desktop/start menu shortcuts. After installation, the app appears in the Windows uninstall list.

Portable executable:

```text
release\快办.exe
```

## Run From Source

Windows and Python 3 are required:

```powershell
python sticky_todo.py
```

You can also run `启动便签.bat`.

## Data Location

User data is stored at:

```text
%APPDATA%\ActNow\data.json
```

## Build

The project is packaged with PyInstaller. See:

```powershell
scripts\build_release.ps1
```

The build script outputs:

```text
release\快办.exe
release\快办安装程序.exe
```

## Author

- Author: Zhijian
- WeChat: vdc089
- GitHub: https://github.com/vodecs001/Act-Now

## Notes

No third-party fonts are bundled. The app icon and QR code are project assets; confirm that you have permission before public distribution.
