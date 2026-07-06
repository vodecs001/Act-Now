import os
import shutil
import subprocess
import sys
import winreg
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox


def _prepare_frozen_tcl() -> None:
    base = getattr(sys, "_MEIPASS", None)
    if not base:
        return

    tcl_candidates = [
        os.environ.get("ACTNOW_TCL_LIBRARY", ""),
        r"E:\inkscape\lib\tcl8.6",
        os.path.join(base, "_tcl_data"),
        os.path.join(base, "lib", "tcl8.6"),
    ]
    tk_candidates = [
        os.environ.get("ACTNOW_TK_LIBRARY", ""),
        r"E:\inkscape\lib\tk8.6",
        os.path.join(base, "_tk_data"),
        os.path.join(base, "lib", "tk8.6"),
    ]

    for candidate in tcl_candidates:
        if os.path.exists(os.path.join(candidate, "init.tcl")):
            os.environ["TCL_LIBRARY"] = candidate.replace("\\", "/")
            break
    for candidate in tk_candidates:
        if os.path.exists(os.path.join(candidate, "tk.tcl")):
            os.environ["TK_LIBRARY"] = candidate.replace("\\", "/")
            break


_prepare_frozen_tcl()


APP_TITLE = "快办"
APP_ENGLISH_NAME = "Act Now"
APP_VERSION = "1.0.0"
PUBLISHER = "执简"
INSTALLER_TITLE = "快办安装程序"
EXE_NAME = "快办.exe"
START_MENU_FOLDER = "快办"
UNINSTALL_REG_KEY = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\ActNow"
COLOR_BG = "#fffbfe"
COLOR_SURFACE = "#f3edf7"
COLOR_PRIMARY = "#4f6356"
COLOR_PRIMARY_HOVER = "#627869"
COLOR_TEXT = "#1d1b20"
COLOR_MUTED = "#79747e"
COLOR_ERROR = "#ba1a1a"
COLOR_ON_PRIMARY = "#ffffff"


def resource_path(relative_path: str) -> Path:
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return base / relative_path


def default_install_dir() -> Path:
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        return Path(local_app_data) / "Programs" / "ActNow"
    return Path.home() / "ActNow"


def ps_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def create_shortcut(shortcut_path: Path, target_path: Path, description: str) -> None:
    shortcut_path.parent.mkdir(parents=True, exist_ok=True)
    script = "\n".join(
        [
            "$shell = New-Object -ComObject WScript.Shell",
            f"$shortcut = $shell.CreateShortcut({ps_quote(str(shortcut_path))})",
            f"$shortcut.TargetPath = {ps_quote(str(target_path))}",
            f"$shortcut.WorkingDirectory = {ps_quote(str(target_path.parent))}",
            f"$shortcut.IconLocation = {ps_quote(str(target_path))}",
            f"$shortcut.Description = {ps_quote(description)}",
            "$shortcut.Save()",
        ]
    )
    subprocess.run(
        ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script],
        check=False,
        creationflags=0x08000000,
    )


def uninstall_command(uninstall_path: Path, quiet: bool = False) -> str:
    suffix = " /quiet" if quiet else ""
    return f'cmd.exe /c ""{uninstall_path}"{suffix}"'


def write_uninstall_registry(install_dir: Path, target_path: Path, uninstall_path: Path) -> None:
    estimated_size_kb = max(1, int((target_path.stat().st_size + uninstall_path.stat().st_size) / 1024))
    with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, UNINSTALL_REG_KEY, 0, winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, f"{APP_TITLE} / {APP_ENGLISH_NAME}")
        winreg.SetValueEx(key, "DisplayVersion", 0, winreg.REG_SZ, APP_VERSION)
        winreg.SetValueEx(key, "Publisher", 0, winreg.REG_SZ, PUBLISHER)
        winreg.SetValueEx(key, "InstallLocation", 0, winreg.REG_SZ, str(install_dir))
        winreg.SetValueEx(key, "DisplayIcon", 0, winreg.REG_SZ, str(target_path))
        winreg.SetValueEx(key, "UninstallString", 0, winreg.REG_SZ, uninstall_command(uninstall_path))
        winreg.SetValueEx(key, "QuietUninstallString", 0, winreg.REG_SZ, uninstall_command(uninstall_path, quiet=True))
        winreg.SetValueEx(key, "EstimatedSize", 0, winreg.REG_DWORD, estimated_size_kb)
        winreg.SetValueEx(key, "NoModify", 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(key, "NoRepair", 0, winreg.REG_DWORD, 1)


def write_uninstaller(install_dir: Path, desktop_shortcut: Path, start_menu_dir: Path) -> Path:
    uninstall_path = install_dir / "卸载快办.cmd"
    lines = [
        "@echo off",
        "chcp 65001 >nul",
        f'reg delete "HKCU\\{UNINSTALL_REG_KEY}" /f >nul 2>nul',
        "taskkill /im 快办.exe /f >nul 2>nul",
        f'del /f /q "{desktop_shortcut}" >nul 2>nul',
        f'rmdir /s /q "{start_menu_dir}" >nul 2>nul',
        f'del /f /q "{install_dir / EXE_NAME}" >nul 2>nul',
        'if /I not "%~1"=="/quiet" echo 快办已卸载。这个窗口可以关闭了。',
        'if /I not "%~1"=="/quiet" pause >nul',
        'del /f /q "%~f0" >nul 2>nul',
    ]
    uninstall_path.write_text("\r\n".join(lines), encoding="utf-8")
    return uninstall_path


class InstallerApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title(INSTALLER_TITLE)
        self.root.geometry("560x310")
        self.root.resizable(False, False)
        self.root.configure(bg=COLOR_BG)
        self.install_dir = tk.StringVar(value=str(default_install_dir()))
        self.desktop_shortcut = tk.BooleanVar(value=True)
        self.start_menu_shortcut = tk.BooleanVar(value=True)
        self.status = tk.StringVar(value="请选择安装目录，然后点击安装。")
        self._apply_icon()
        self._build()

    def _apply_icon(self) -> None:
        icon_path = resource_path("assets/app_icon.ico")
        png_path = resource_path("assets/app_icon_256.png")
        try:
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
            if png_path.exists():
                self.icon_image = tk.PhotoImage(file=str(png_path))
                self.root.iconphoto(True, self.icon_image)
        except tk.TclError:
            pass

    def _button(self, parent, text: str, command, primary: bool = False) -> tk.Button:
        bg = COLOR_PRIMARY if primary else COLOR_SURFACE
        fg = COLOR_ON_PRIMARY if primary else COLOR_TEXT
        hover = COLOR_PRIMARY_HOVER if primary else "#ece6f0"
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=hover,
            activeforeground=fg,
            relief="flat",
            bd=0,
            padx=14,
            pady=6,
            cursor="hand2",
        )
        button.bind("<Enter>", lambda _event: button.configure(bg=hover))
        button.bind("<Leave>", lambda _event: button.configure(bg=bg))
        return button

    def _build(self) -> None:
        tk.Label(
            self.root,
            text=f"{APP_TITLE} / {APP_ENGLISH_NAME}",
            bg=COLOR_BG,
            fg=COLOR_TEXT,
            font=("TkDefaultFont", 18, "bold"),
        ).pack(anchor="w", padx=24, pady=(22, 4))
        tk.Label(
            self.root,
            text="选择安装目录后，安装程序会复制主程序并创建快捷方式。",
            bg=COLOR_BG,
            fg=COLOR_MUTED,
        ).pack(anchor="w", padx=24, pady=(0, 18))

        path_row = tk.Frame(self.root, bg=COLOR_BG)
        path_row.pack(fill="x", padx=24)
        path_shell = tk.Frame(path_row, bg=COLOR_SURFACE, highlightbackground="#cac4d0", highlightthickness=1)
        path_shell.pack(side="left", fill="x", expand=True)
        tk.Entry(
            path_shell,
            textvariable=self.install_dir,
            relief="flat",
            bg=COLOR_SURFACE,
            fg=COLOR_TEXT,
            insertbackground=COLOR_TEXT,
            bd=0,
        ).pack(fill="x", padx=10, ipady=8)
        self._button(path_row, "浏览", self.browse).pack(side="left", padx=(10, 0))

        options = tk.Frame(self.root, bg=COLOR_BG)
        options.pack(fill="x", padx=24, pady=(18, 0))
        tk.Checkbutton(
            options,
            text="创建桌面快捷方式",
            variable=self.desktop_shortcut,
            bg=COLOR_BG,
            fg=COLOR_TEXT,
            activebackground=COLOR_BG,
            selectcolor=COLOR_SURFACE,
        ).pack(anchor="w")
        tk.Checkbutton(
            options,
            text="创建开始菜单快捷方式",
            variable=self.start_menu_shortcut,
            bg=COLOR_BG,
            fg=COLOR_TEXT,
            activebackground=COLOR_BG,
            selectcolor=COLOR_SURFACE,
        ).pack(anchor="w")

        tk.Label(self.root, textvariable=self.status, bg=COLOR_BG, fg=COLOR_MUTED).pack(anchor="w", padx=24, pady=(18, 0))

        actions = tk.Frame(self.root, bg=COLOR_BG)
        actions.pack(fill="x", padx=24, pady=(18, 0))
        self._button(actions, "退出", self.root.destroy).pack(side="right")
        self._button(actions, "安装", self.install, primary=True).pack(side="right", padx=(0, 10))

    def browse(self) -> None:
        selected = filedialog.askdirectory(initialdir=self.install_dir.get() or str(default_install_dir()))
        if selected:
            self.install_dir.set(selected)

    def install(self) -> None:
        payload = resource_path(f"payload/{EXE_NAME}")
        if not payload.exists():
            messagebox.showerror(INSTALLER_TITLE, "安装包缺少主程序文件。")
            return

        install_dir = Path(self.install_dir.get()).expanduser()
        if not str(install_dir).strip():
            messagebox.showerror(INSTALLER_TITLE, "请选择安装目录。")
            return

        try:
            install_dir.mkdir(parents=True, exist_ok=True)
            target = install_dir / EXE_NAME
            shutil.copy2(payload, target)

            desktop_link = Path(os.environ.get("USERPROFILE", str(Path.home()))) / "Desktop" / "快办.lnk"
            start_menu_dir = Path(os.environ.get("APPDATA", str(Path.home()))) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / START_MENU_FOLDER
            start_menu_link = start_menu_dir / "快办.lnk"

            if self.desktop_shortcut.get():
                create_shortcut(desktop_link, target, "快办 / Act Now")
            if self.start_menu_shortcut.get():
                create_shortcut(start_menu_link, target, "快办 / Act Now")

            uninstall_path = write_uninstaller(install_dir, desktop_link, start_menu_dir)
            write_uninstall_registry(install_dir, target, uninstall_path)
        except OSError as exc:
            messagebox.showerror(INSTALLER_TITLE, f"安装失败：{exc}")
            return

        self.status.set(f"安装完成：{install_dir}")
        if messagebox.askyesno(INSTALLER_TITLE, "安装完成，是否现在启动快办？"):
            subprocess.Popen([str(install_dir / EXE_NAME)], cwd=str(install_dir))
        self.root.destroy()

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    InstallerApp().run()


if __name__ == "__main__":
    main()
