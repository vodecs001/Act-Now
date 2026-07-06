# Act Now

Act Now is a lightweight Windows desktop sticky todo app for keeping daily tasks close at hand near the screen edge, with quick add, complete, edit, and archive workflows.

## Current Release

Only the portable edition is provided now. There is no installer edition.

```text
release\快办-免安装.exe
```

Double-click the executable to run it. If an older copy is already running, exit it first before opening the new portable build.

## Features

- Todos: add, complete, edit, delete, and automatically archive completed tasks.
- Todo editing: use the pencil icon beside each todo, or double-click the todo text to edit it.
- Creation time: each todo shows its creation time in the lower-left corner.
- Groups: use All Todos or custom groups; deleting a group keeps its todos in All Todos.
- Legacy default group cleanup: old `默认 / inbox` group data is migrated away automatically so the sidebar no longer shows an undeletable default group.
- Archive: restore completed todos, delete individual archived items, or clear the whole archive.
- Edge hide: supports left, right, and top edge hiding; the bottom edge does not trigger hiding.
- Top auto-hide: drag the window to the top of the screen to hide it, then move the pointer near the top edge to reveal it.
- Window controls: drag to move, drag to resize, minimize to the taskbar, or configure the close button to exit or minimize to tray.
- Startup: optional start with Windows.
- Languages: Chinese, English, and Japanese. The main UI and tray menu follow the selected language.
- Material You style: light surfaces, soft container colors, clear input field, and hover highlights on title-bar buttons.
- Taskbar and tray: the app appears in both the Windows taskbar and system tray.

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

Copying or replacing the project folder does not clear this user data. The current version automatically migrates legacy default group data on startup.

## Build

The current release keeps only the portable executable:

```text
release\快办-免安装.exe
```

The project is packaged with PyInstaller. See:

```powershell
scripts\build_release.ps1
```

## Author

- Author: Zhijian
- WeChat: vdc089
- GitHub: https://github.com/vodecs001/Act-Now

## Notes

No third-party fonts are bundled. The app icon and QR code are project assets; confirm that you have permission before public distribution.