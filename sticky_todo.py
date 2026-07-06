import ctypes
import json
import os
import subprocess
import sys
import uuid
import webbrowser
import winreg
from ctypes import wintypes
from datetime import datetime
from pathlib import Path


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

import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, simpledialog

if not hasattr(wintypes, "HICON"):
    wintypes.HICON = wintypes.HANDLE
if not hasattr(wintypes, "HCURSOR"):
    wintypes.HCURSOR = wintypes.HANDLE
if not hasattr(wintypes, "HBRUSH"):
    wintypes.HBRUSH = wintypes.HANDLE


APP_NAME = "ActNow"
APP_TITLE = "快办"
APP_ENGLISH_NAME = "Act Now"
APP_USER_MODEL_ID = "ZJ.ActNow"
AUTHOR = "执简"
WECHAT = "vdc089"
GITHUB_URL = "https://github.com/vodecs001/Act-Now"
COLOR_BG = "#fffbfe"
COLOR_SURFACE = "#fffbfe"
COLOR_SURFACE_CONTAINER = "#f3edf7"
COLOR_SURFACE_HIGH = "#ece6f0"
COLOR_OUTLINE = "#cac4d0"
COLOR_PRIMARY = "#4f6356"
COLOR_PRIMARY_HOVER = "#627869"
COLOR_ON_PRIMARY = "#ffffff"
COLOR_TEXT = "#1d1b20"
COLOR_MUTED = "#79747e"
COLOR_AUTHOR_TEXT = "#d6e8d8"
COLOR_CLOSE_TEXT = "#ffe8dd"
COLOR_ERROR = "#ba1a1a"
COLOR_ERROR_CONTAINER = "#ffdad6"
COLOR_ERROR_HOVER = "#ffd1cc"
ALL_GROUPS_ID = "all"
DEFAULT_GROUP_ID = "inbox"
EDGE_STRIP = 1
TOP_EDGE_STRIP = 1
TOP_HOT_ZONE = 28
TOP_POP_MARGIN = 36
EDGE_THRESHOLD = 8
HIDE_DELAY_MS = 700
AUTO_HIDE_AFTER_SNAP_MS = 360
ANIMATION_STEPS = 10
ANIMATION_INTERVAL_MS = 12
DEFAULT_WIDTH = 520
DEFAULT_HEIGHT = 520
MIN_WIDTH = 420
MIN_HEIGHT = 360
VALID_SNAP_EDGES = {"left", "right", "top"}
CLOSE_ACTION_EXIT = "exit"
CLOSE_ACTION_MINIMIZE = "minimize"
VALID_CLOSE_ACTIONS = {CLOSE_ACTION_EXIT, CLOSE_ACTION_MINIMIZE}

LANGUAGES = {
    "zh": {
        "all_todos": "所有待办",
        "archive": "归档",
        "help": "帮助",
        "hide": "收起",
        "minimize": "最小化",
        "settings_edge_hide": "贴边隐藏",
        "settings_topmost": "窗口置顶",
        "settings_startup": "开机自启动",
        "settings_close_action": "关闭按钮",
        "close_action_exit": "退出程序",
        "close_action_minimize": "最小化到托盘",
        "settings_language": "语言",
        "language_zh": "中文",
        "language_en": "英文",
        "language_ja": "日文",
        "about_author": "关于作者",
        "author_title": "作者:执简",
        "author": "作者",
        "wechat": "微信",
        "close": "关闭",
        "archive_title": "已完成待办",
        "archive_empty": "还没有已完成的待办",
        "clear_archive": "清空归档",
        "clear_archive_confirm_title": "清空归档",
        "clear_archive_confirm": "确定要删除所有已完成的待办吗？",
        "restore": "恢复",
        "empty": "今天还没有待办",
        "todo_summary": "待办 {open} / 归档 {archived}",
        "created_at": "创建 {time}",
        "qr_missing": "二维码暂时无法显示",
        "startup_error_title": "开机自启动",
        "startup_error": "启动项设置失败：{error}",
        "default_group": "默认",
        "new_group": "新分组",
        "new_group_prompt": "请输入分组名称",
        "delete_group": "删除分组",
        "delete_group_confirm_title": "删除分组",
        "delete_group_confirm": "确定删除“{group}”吗？该分组下的待办会移到默认分组。",
        "tray_tip": "快办 / Act Now",
        "tray_show": "显示快办",
        "tray_exit": "退出快办",
        "system_windows_only": "这个版本主要为 Windows 桌面设计。",
    },
    "en": {
        "all_todos": "All",
        "archive": "Archive",
        "help": "Help",
        "hide": "Hide",
        "minimize": "Minimize",
        "settings_edge_hide": "Edge hide",
        "settings_topmost": "Always on top",
        "settings_startup": "Start with Windows",
        "settings_close_action": "Close button",
        "close_action_exit": "Exit app",
        "close_action_minimize": "Minimize to tray",
        "settings_language": "Language",
        "language_zh": "Chinese",
        "language_en": "English",
        "language_ja": "Japanese",
        "about_author": "About Author",
        "author_title": "Author: Zhijian",
        "author": "Author",
        "wechat": "WeChat",
        "close": "Close",
        "archive_title": "Completed",
        "archive_empty": "No completed todos yet",
        "clear_archive": "Clear archive",
        "clear_archive_confirm_title": "Clear archive",
        "clear_archive_confirm": "Delete all completed todos?",
        "restore": "Restore",
        "empty": "No todos today",
        "todo_summary": "Todos {open} / Archived {archived}",
        "created_at": "Created {time}",
        "qr_missing": "QR code unavailable",
        "startup_error_title": "Startup",
        "startup_error": "Failed to update startup setting: {error}",
        "default_group": "Default",
        "new_group": "New group",
        "new_group_prompt": "Enter group name",
        "delete_group": "Delete group",
        "delete_group_confirm_title": "Delete group",
        "delete_group_confirm": "Delete “{group}”? Todos in it will move to Default.",
        "tray_tip": "Act Now",
        "tray_show": "Show Act Now",
        "tray_exit": "Exit Act Now",
        "system_windows_only": "This version is designed for Windows desktop.",
    },
    "ja": {
        "all_todos": "すべて",
        "archive": "アーカイブ",
        "help": "ヘルプ",
        "hide": "隠す",
        "minimize": "最小化",
        "settings_edge_hide": "端に隠す",
        "settings_topmost": "常に前面",
        "settings_startup": "自動起動",
        "settings_close_action": "閉じるボタン",
        "close_action_exit": "終了する",
        "close_action_minimize": "トレイに最小化",
        "settings_language": "言語",
        "language_zh": "中国語",
        "language_en": "英語",
        "language_ja": "日本語",
        "about_author": "作者について",
        "author_title": "作者: 執簡",
        "author": "作者",
        "wechat": "WeChat",
        "close": "閉じる",
        "archive_title": "完了済み",
        "archive_empty": "完了したタスクはまだありません",
        "clear_archive": "アーカイブを空にする",
        "clear_archive_confirm_title": "アーカイブを空にする",
        "clear_archive_confirm": "完了済みタスクをすべて削除しますか？",
        "restore": "戻す",
        "empty": "今日のタスクはありません",
        "todo_summary": "未完了 {open} / アーカイブ {archived}",
        "created_at": "作成 {time}",
        "qr_missing": "QRコードを表示できません",
        "startup_error_title": "自動起動",
        "startup_error": "自動起動の設定に失敗しました: {error}",
        "default_group": "デフォルト",
        "new_group": "新規グループ",
        "new_group_prompt": "グループ名を入力してください",
        "delete_group": "グループを削除",
        "delete_group_confirm_title": "グループを削除",
        "delete_group_confirm": "「{group}」を削除しますか？このグループのタスクはデフォルトへ移動します。",
        "tray_tip": "快办 / Act Now",
        "tray_show": "快办を表示",
        "tray_exit": "快办を終了",
        "system_windows_only": "このバージョンは Windows デスクトップ向けです。",
    },
}

GWL_EXSTYLE = -20
WS_EX_TOOLWINDOW = 0x00000080
WS_EX_APPWINDOW = 0x00040000
SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001
SWP_NOZORDER = 0x0004
SWP_FRAMECHANGED = 0x0020
GA_ROOT = 2
NIM_ADD = 0x00000000
NIM_DELETE = 0x00000002
NIF_MESSAGE = 0x00000001
NIF_ICON = 0x00000002
NIF_TIP = 0x00000004
WM_APP = 0x8000
WM_LBUTTONUP = 0x0202
WM_LBUTTONDBLCLK = 0x0203
WM_RBUTTONUP = 0x0205
IDI_APPLICATION = 32512


WNDPROC = ctypes.WINFUNCTYPE(
    wintypes.LPARAM,
    wintypes.HWND,
    wintypes.UINT,
    wintypes.WPARAM,
    wintypes.LPARAM,
)


class WNDCLASSW(ctypes.Structure):
    _fields_ = [
        ("style", wintypes.UINT),
        ("lpfnWndProc", WNDPROC),
        ("cbClsExtra", ctypes.c_int),
        ("cbWndExtra", ctypes.c_int),
        ("hInstance", wintypes.HINSTANCE),
        ("hIcon", wintypes.HICON),
        ("hCursor", wintypes.HCURSOR),
        ("hbrBackground", wintypes.HBRUSH),
        ("lpszMenuName", wintypes.LPCWSTR),
        ("lpszClassName", wintypes.LPCWSTR),
    ]


class NOTIFYICONDATAW(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("hWnd", wintypes.HWND),
        ("uID", wintypes.UINT),
        ("uFlags", wintypes.UINT),
        ("uCallbackMessage", wintypes.UINT),
        ("hIcon", wintypes.HICON),
        ("szTip", wintypes.WCHAR * 128),
        ("dwState", wintypes.DWORD),
        ("dwStateMask", wintypes.DWORD),
        ("szInfo", wintypes.WCHAR * 256),
        ("uTimeoutOrVersion", wintypes.UINT),
        ("szInfoTitle", wintypes.WCHAR * 64),
        ("dwInfoFlags", wintypes.DWORD),
    ]


class NOTIFYICONDATA_BASICW(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("hWnd", wintypes.HWND),
        ("uID", wintypes.UINT),
        ("uFlags", wintypes.UINT),
        ("uCallbackMessage", wintypes.UINT),
        ("hIcon", wintypes.HICON),
        ("szTip", wintypes.WCHAR * 128),
    ]


def resource_path(relative_path: str) -> Path:
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return base / relative_path


def app_dir() -> Path:
    base = os.environ.get("APPDATA")
    if base:
        path = Path(base) / APP_NAME
    else:
        path = Path.home() / f".{APP_NAME}"
    path.mkdir(parents=True, exist_ok=True)
    return path


DATA_FILE = app_dir() / "data.json"


class RECT(ctypes.Structure):
    _fields_ = [
        ("left", ctypes.c_long),
        ("top", ctypes.c_long),
        ("right", ctypes.c_long),
        ("bottom", ctypes.c_long),
    ]


def work_area(root: tk.Tk) -> tuple[int, int, int, int]:
    rect = RECT()
    ok = ctypes.windll.user32.SystemParametersInfoW(0x0030, 0, ctypes.byref(rect), 0)
    if ok:
        return rect.left, rect.top, rect.right, rect.bottom
    return 0, 0, root.winfo_screenwidth(), root.winfo_screenheight()


def window_rect(root: tk.Tk) -> tuple[int, int, int, int]:
    if sys.platform == "win32":
        rect = RECT()
        hwnd = wintypes.HWND(root.winfo_id())
        if ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect)):
            return rect.left, rect.top, rect.right, rect.bottom
    x = root.winfo_x()
    y = root.winfo_y()
    return x, y, x + root.winfo_width(), y + root.winfo_height()


def clamp(value: int, low: int, high: int) -> int:
    return max(low, min(value, high))


class Startup:
    RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"

    @staticmethod
    def command() -> str:
        if getattr(sys, "frozen", False):
            return f'"{sys.executable}"'

        executable = Path(sys.executable)
        pythonw = executable.with_name("pythonw.exe")
        runner = pythonw if pythonw.exists() else executable
        script = Path(__file__).resolve()
        return f'"{runner}" "{script}"'

    @classmethod
    def is_enabled(cls) -> bool:
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, cls.RUN_KEY, 0, winreg.KEY_READ) as key:
                value, _ = winreg.QueryValueEx(key, APP_NAME)
            return value == cls.command()
        except FileNotFoundError:
            return False
        except OSError:
            return False

    @classmethod
    def set_enabled(cls, enabled: bool) -> None:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            cls.RUN_KEY,
            0,
            winreg.KEY_SET_VALUE,
        ) as key:
            if enabled:
                winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, cls.command())
            else:
                try:
                    winreg.DeleteValue(key, APP_NAME)
                except FileNotFoundError:
                    pass


class Store:
    def __init__(self) -> None:
        self.items: list[dict] = []
        self.groups: list[dict] = []
        self.settings = {
            "width": DEFAULT_WIDTH,
            "height": DEFAULT_HEIGHT,
            "x": 80,
            "y": 80,
            "edge_hide": True,
            "topmost": False,
            "topmost_explicit": False,
            "snapped_edge": None,
            "selected_group_id": ALL_GROUPS_ID,
            "language": "zh",
            "close_action": CLOSE_ACTION_EXIT,
        }
        self.load()

    def load(self) -> None:
        if not DATA_FILE.exists():
            created_at = self.now_iso()
            self.groups = [{"id": DEFAULT_GROUP_ID, "name": self.default_group_name()}]
            self.items = [
                {
                    "id": self.new_id(),
                    "text": "写下第一件要做的事",
                    "done": False,
                    "group_id": DEFAULT_GROUP_ID,
                    "created_at": created_at,
                },
                {
                    "id": self.new_id(),
                    "text": "拖到屏幕边缘试试贴边隐藏",
                    "done": False,
                    "group_id": DEFAULT_GROUP_ID,
                    "created_at": created_at,
                },
            ]
            return

        try:
            payload = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return

        if isinstance(payload.get("groups"), list):
            self.groups = [
                {"id": str(group.get("id") or self.new_id()), "name": str(group.get("name") or self.default_group_name())}
                for group in payload["groups"]
                if isinstance(group, dict)
            ]
        if not self.groups:
            self.groups = [{"id": DEFAULT_GROUP_ID, "name": self.default_group_name()}]

        valid_group_ids = {group["id"] for group in self.groups}

        if isinstance(payload.get("items"), list):
            self.items = []
            for item in payload["items"]:
                if isinstance(item, dict) and isinstance(item.get("text"), str):
                    group_id = str(item.get("group_id") or self.groups[0]["id"])
                    if group_id not in valid_group_ids:
                        group_id = self.groups[0]["id"]
                    self.items.append(
                        {
                            "id": str(item.get("id") or self.new_id()),
                            "text": item["text"],
                            "done": bool(item.get("done")),
                            "group_id": group_id,
                            "created_at": str(item.get("created_at") or self.now_iso()),
                        }
                    )
        if isinstance(payload.get("settings"), dict):
            self.settings.update(payload["settings"])
        if self.settings.get("language") not in LANGUAGES:
            self.settings["language"] = "zh"
        if self.settings.get("close_action") not in VALID_CLOSE_ACTIONS:
            self.settings["close_action"] = CLOSE_ACTION_EXIT
        if not self.settings.get("topmost_explicit"):
            self.settings["topmost"] = False
        selected_group_id = self.settings.get("selected_group_id")
        if selected_group_id != ALL_GROUPS_ID and selected_group_id not in valid_group_ids:
            self.settings["selected_group_id"] = ALL_GROUPS_ID

    def save(self) -> None:
        payload = {"items": self.items, "groups": self.groups, "settings": self.settings}
        DATA_FILE.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    @staticmethod
    def new_id() -> str:
        return uuid.uuid4().hex

    @staticmethod
    def now_iso() -> str:
        return datetime.now().isoformat(timespec="minutes")

    @staticmethod
    def default_group_name() -> str:
        return LANGUAGES["zh"]["default_group"]


class TodoApp:
    def __init__(self) -> None:
        self.store = Store()
        self._set_app_user_model_id()
        self.root = tk.Tk()
        self.root.title(f"{APP_TITLE} / {APP_ENGLISH_NAME}")
        self.root.overrideredirect(True)
        self.root.configure(bg=COLOR_BG)
        self.root.minsize(MIN_WIDTH, MIN_HEIGHT)
        self._apply_window_icon()
        self._init_fonts()

        self.drag_offset = (0, 0)
        self.dragging = False
        self.resize_start = None
        self.snapped_edge = self.store.settings.get("snapped_edge")
        if self.snapped_edge not in VALID_SNAP_EDGES:
            self.snapped_edge = None
        self.hidden = False
        self.hide_after_id = None
        self.animation_after_id = None
        self.snap_after_id = None
        self.tray_hwnd = None
        self.tray_icon_added = False
        self.tray_process = None
        self.taskbar_proxy = None
        self.restore_signal_path = app_dir() / "restore.signal"
        self.last_normal_geometry = None
        self.restoring_from_zoom = False
        self.programmatic_move = False
        self.edge_reveal_ready = True
        self.taskbar_ready = False
        self.closing = False
        self.minimized_by_close = False
        self.minimized_to_taskbar = False

        self.edge_hide = tk.BooleanVar(value=bool(self.store.settings.get("edge_hide", True)))
        self.topmost = tk.BooleanVar(value=bool(self.store.settings.get("topmost", False)))
        self.startup = tk.BooleanVar(value=Startup.is_enabled())
        self.language = tk.StringVar(value=self.store.settings.get("language", "zh"))
        self.close_action = tk.StringVar(value=self.store.settings.get("close_action", CLOSE_ACTION_EXIT))
        self.new_text = tk.StringVar()
        self.selected_group_id = str(self.store.settings.get("selected_group_id", ALL_GROUPS_ID))

        self._build()
        self._restore_geometry()
        self._apply_topmost()

        self.root.bind("<Enter>", self._on_enter)
        self.root.bind("<Leave>", self._on_leave)
        self.root.bind("<Configure>", self._on_configure)
        self.root.protocol("WM_DELETE_WINDOW", self.request_close)
        self.root.after(150, self._create_tray_icon)
        self.root.after(200, self._show_in_taskbar)
        self.root.after(300, self._maybe_hide_after_start)
        self.root.after(250, self._poll_top_autohide)
        self.root.after(700, self._poll_restore_signal)

    def _init_fonts(self) -> None:
        self.font_ui = tkfont.nametofont("TkDefaultFont")
        self.font_small = self.font_ui.copy()
        self.font_small.configure(size=max(8, self.font_ui.cget("size") - 1))
        self.font_title = self.font_ui.copy()
        self.font_title.configure(weight="bold")
        self.font_tool = self.font_ui.copy()
        self.font_tool.configure(size=max(9, self.font_ui.cget("size")), weight="bold")
        self.font_icon = self.font_ui.copy()
        self.font_icon.configure(size=self.font_ui.cget("size") + 3, weight="bold")
        self.font_close = self.font_ui.copy()
        self.font_close.configure(size=self.font_ui.cget("size") + 5, weight="bold")
        self.font_author = self.font_ui.copy()
        self.font_author.configure(size=max(8, self.font_ui.cget("size") - 1), weight="bold")
        self.font_big = self.font_ui.copy()
        self.font_big.configure(size=self.font_ui.cget("size") + 2, weight="bold")
        self.font_done = self.font_ui.copy()
        self.font_done.configure(overstrike=True)

    def _set_app_user_model_id(self) -> None:
        if sys.platform != "win32":
            return
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_USER_MODEL_ID)
        except OSError:
            pass

    def t(self, key: str, **kwargs) -> str:
        language = self.language.get() if hasattr(self, "language") else self.store.settings.get("language", "zh")
        template = LANGUAGES.get(language, LANGUAGES["zh"]).get(key, LANGUAGES["zh"].get(key, key))
        return template.format(**kwargs) if kwargs else template

    def group_name(self, group_id: str) -> str:
        if group_id == ALL_GROUPS_ID:
            return self.t("all_todos")
        for group in self.store.groups:
            if group["id"] == group_id:
                if group["id"] == DEFAULT_GROUP_ID and group["name"] == LANGUAGES["zh"]["default_group"]:
                    return self.t("default_group")
                return group["name"]
        return self.t("default_group")

    def format_created_at(self, value: str) -> str:
        try:
            created = datetime.fromisoformat(str(value))
        except ValueError:
            created = datetime.now()
        if created.year == datetime.now().year:
            return created.strftime("%m-%d %H:%M")
        return created.strftime("%Y-%m-%d %H:%M")

    def _title_button(
        self,
        parent,
        text: str,
        width: int,
        command,
        font=None,
        fg: str = COLOR_ON_PRIMARY,
        hover_bg: str = COLOR_PRIMARY_HOVER,
        hover_fg: str = COLOR_ON_PRIMARY,
    ) -> tk.Button:
        button = tk.Button(
            parent,
            text=text,
            width=width,
            height=1,
            bg=COLOR_PRIMARY,
            fg=fg,
            activebackground=COLOR_PRIMARY_HOVER,
            activeforeground=COLOR_ON_PRIMARY,
            relief="flat",
            bd=0,
            highlightthickness=0,
            padx=0,
            pady=0,
            anchor="center",
            font=font or self.font_tool,
            cursor="hand2",
            command=command,
        )
        button.bind("<Enter>", lambda _event: button.configure(bg=hover_bg, fg=hover_fg))
        button.bind("<Leave>", lambda _event: button.configure(bg=COLOR_PRIMARY, fg=fg))
        return button

    def _build(self) -> None:
        title_bar = tk.Frame(self.root, bg=COLOR_PRIMARY, height=44)
        title_bar.pack(fill="x")
        title_bar.pack_propagate(False)
        title_bar.grid_propagate(False)
        title_bar.grid_columnconfigure(0, minsize=224)
        title_bar.grid_columnconfigure(1, weight=1)
        title_bar.grid_columnconfigure(2, minsize=104)
        title_bar.grid_rowconfigure(0, weight=1)
        title_bar.bind("<ButtonPress-1>", self._start_drag)
        title_bar.bind("<B1-Motion>", self._drag)
        title_bar.bind("<ButtonRelease-1>", self._end_drag)

        left_tools = tk.Frame(title_bar, bg=COLOR_PRIMARY)
        left_tools.grid(row=0, column=0, sticky="nsw", padx=(6, 0))

        settings_btn = self._title_button(left_tools, "⚙", 3, self.show_settings_menu, font=self.font_icon)
        settings_btn.pack(side="left", fill="y", pady=5)

        archive_btn = self._title_button(left_tools, self.t("archive"), 6, self.show_archive)
        archive_btn.pack(side="left", fill="y", padx=(4, 0), pady=6)

        github_btn = self._title_button(left_tools, "GitHub", 8, self.open_github)
        github_btn.pack(side="left", fill="y", padx=(2, 0), pady=6)

        help_btn = self._title_button(left_tools, self.t("help"), 5, self.show_help_menu)
        help_btn.pack(side="left", fill="y", padx=(2, 0), pady=6)

        author_title = tk.Label(
            title_bar,
            text=self.t("author_title"),
            bg=COLOR_PRIMARY,
            fg=COLOR_AUTHOR_TEXT,
            anchor="center",
            font=self.font_author,
        )
        author_title.grid(row=0, column=1, sticky="nsew", pady=(2, 0))
        author_title.bind("<ButtonPress-1>", self._start_drag)
        author_title.bind("<B1-Motion>", self._drag)
        author_title.bind("<ButtonRelease-1>", self._end_drag)

        right_tools = tk.Frame(title_bar, bg=COLOR_PRIMARY)
        right_tools.grid(row=0, column=2, sticky="nse", padx=(0, 6))

        close_btn = self._title_button(
            right_tools,
            "×",
            3,
            self.request_close,
            font=self.font_close,
            fg=COLOR_CLOSE_TEXT,
            hover_bg=COLOR_ERROR,
            hover_fg=COLOR_ON_PRIMARY,
        )
        close_btn.pack(side="right", fill="y", pady=5)

        hide_btn = self._title_button(right_tools, self.t("hide"), 5, self.hide_to_nearest_edge)
        hide_btn.pack(side="right", fill="y", padx=(0, 4), pady=6)

        minimize_btn = self._title_button(right_tools, "—", 3, self.minimize_to_taskbar, font=self.font_tool)
        minimize_btn.pack(side="right", fill="y", padx=(0, 4), pady=6)

        content = tk.Frame(self.root, bg=COLOR_BG)
        content.pack(fill="both", expand=True, padx=12, pady=(12, 14))

        self.sidebar_frame = tk.Frame(content, bg=COLOR_SURFACE_CONTAINER, width=132)
        self.sidebar_frame.pack(side="left", fill="y", padx=(0, 10))
        self.sidebar_frame.pack_propagate(False)

        main_panel = tk.Frame(content, bg=COLOR_BG)
        main_panel.pack(side="left", fill="both", expand=True)

        entry_row = tk.Frame(main_panel, bg=COLOR_BG)
        entry_row.pack(fill="x", pady=(0, 10))

        input_shell = tk.Frame(
            entry_row,
            bg=COLOR_SURFACE_CONTAINER,
            highlightbackground=COLOR_OUTLINE,
            highlightcolor=COLOR_PRIMARY,
            highlightthickness=1,
            bd=0,
        )
        input_shell.pack(side="left", fill="x", expand=True)

        entry = tk.Entry(
            input_shell,
            textvariable=self.new_text,
            relief="flat",
            bg=COLOR_SURFACE_CONTAINER,
            fg=COLOR_TEXT,
            insertbackground=COLOR_TEXT,
            font=self.font_ui,
            bd=0,
            highlightthickness=0,
        )
        entry.pack(fill="x", expand=True, padx=10, ipady=8)
        entry.bind("<Return>", lambda _event: self.add_item())
        entry.bind("<FocusIn>", lambda _event: input_shell.configure(highlightbackground=COLOR_PRIMARY))
        entry.bind("<FocusOut>", lambda _event: input_shell.configure(highlightbackground=COLOR_OUTLINE))

        add_btn = tk.Button(
            entry_row,
            text="+",
            width=4,
            bg=COLOR_PRIMARY,
            fg=COLOR_ON_PRIMARY,
            activebackground=COLOR_PRIMARY_HOVER,
            activeforeground=COLOR_ON_PRIMARY,
            relief="flat",
            font=self.font_big,
            command=self.add_item,
        )
        add_btn.pack(side="left", padx=(8, 0), ipady=2)

        list_area = tk.Frame(main_panel, bg=COLOR_BG)
        list_area.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(list_area, bg=COLOR_BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(list_area, orient="vertical", command=self.canvas.yview)
        self.list_frame = tk.Frame(self.canvas, bg=COLOR_BG)
        self.list_frame.bind(
            "<Configure>",
            lambda _event: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.list_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y", padx=(6, 0))
        self.canvas.bind("<Configure>", self._resize_list)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        footer = tk.Frame(self.root, bg=COLOR_SURFACE_HIGH, height=7, cursor="sb_v_double_arrow")
        footer.pack(fill="x", side="bottom")
        footer.bind("<ButtonPress-1>", lambda event: self._start_resize(event, "bottom"))
        footer.bind("<B1-Motion>", self._resize)
        footer.bind("<ButtonRelease-1>", self._end_drag)

        self._add_resize_handles()
        self.render_groups()
        self.render_items()

    def _checkbutton(self, parent, text, variable, command):
        return tk.Checkbutton(
            parent,
            text=text,
            variable=variable,
            command=command,
            bg=COLOR_BG,
            fg=COLOR_TEXT,
            activebackground=COLOR_BG,
            activeforeground=COLOR_TEXT,
            selectcolor=COLOR_SURFACE,
            font=self.font_small,
        )

    def _show_in_taskbar(self) -> None:
        if sys.platform != "win32":
            return
        try:
            self._set_app_user_model_id()
            if self.taskbar_proxy is None or not self.taskbar_proxy.winfo_exists():
                self.taskbar_proxy = tk.Toplevel(self.root)
                self.taskbar_proxy.title(f"{APP_TITLE} / {APP_ENGLISH_NAME}")
                self.taskbar_proxy.geometry("1x1+-32000+-32000")
                self.taskbar_proxy.resizable(False, False)
                self.taskbar_proxy.protocol("WM_DELETE_WINDOW", self.request_close)
                self.taskbar_proxy.bind("<Map>", self._on_taskbar_proxy_map)
                self._apply_window_icon(self.taskbar_proxy)
                self.taskbar_proxy.update_idletasks()
            self._mark_taskbar_window(self.taskbar_proxy)
            self.taskbar_ready = True
        except (OSError, tk.TclError):
            pass

    def _mark_taskbar_window(self, window: tk.Toplevel) -> None:
        user32 = ctypes.windll.user32
        hwnd = user32.GetAncestor(wintypes.HWND(window.winfo_id()), GA_ROOT)
        if not hwnd:
            hwnd = window.winfo_id()
        hwnd = wintypes.HWND(hwnd)
        get_window_long = getattr(user32, "GetWindowLongPtrW", user32.GetWindowLongW)
        set_window_long = getattr(user32, "SetWindowLongPtrW", user32.SetWindowLongW)
        ex_style = get_window_long(hwnd, GWL_EXSTYLE)
        ex_style = (ex_style & ~WS_EX_TOOLWINDOW) | WS_EX_APPWINDOW
        set_window_long(hwnd, GWL_EXSTYLE, ex_style)
        user32.SetWindowPos(
            hwnd,
            None,
            0,
            0,
            0,
            0,
            SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED,
        )

    def _finish_taskbar_refresh(self) -> None:
        try:
            self.root.deiconify()
            self._apply_topmost()
        except tk.TclError:
            pass

    def _create_tray_icon(self) -> None:
        if sys.platform != "win32" or self.tray_process:
            return

        icon_path = resource_path("assets/app_icon.ico")
        if not icon_path.exists():
            return

        script_path = app_dir() / "tray_icon.ps1"
        script_path.write_text(
            r'''
param(
    [int]$AppPid,
    [string]$IconPath,
    [string]$SignalPath,
    [string]$Tooltip,
    [string]$ShowText,
    [string]$ExitText
)

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class WinApi {
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
}
"@

$notify = New-Object System.Windows.Forms.NotifyIcon
$notify.Icon = New-Object System.Drawing.Icon($IconPath)
$notify.Text = $Tooltip
$notify.Visible = $true

$showItem = New-Object System.Windows.Forms.MenuItem
$showItem.Text = $ShowText
$exitItem = New-Object System.Windows.Forms.MenuItem
$exitItem.Text = $ExitText
$menu = New-Object System.Windows.Forms.ContextMenu
[void]$menu.MenuItems.Add($showItem)
[void]$menu.MenuItems.Add($exitItem)
$notify.ContextMenu = $menu

$showAction = {
    try {
        Set-Content -Path $SignalPath -Value ([DateTime]::Now.Ticks) -Encoding UTF8
        $p = Get-Process -Id $AppPid -ErrorAction Stop
        if ($p.MainWindowHandle -ne 0) {
            [WinApi]::ShowWindow($p.MainWindowHandle, 9) | Out-Null
            [WinApi]::SetForegroundWindow($p.MainWindowHandle) | Out-Null
        }
    } catch {}
}

$notify.add_DoubleClick($showAction)
$showItem.add_Click($showAction)
$exitItem.add_Click({
    try { Stop-Process -Id $AppPid -ErrorAction SilentlyContinue } catch {}
    $notify.Visible = $false
    [System.Windows.Forms.Application]::Exit()
})

$timer = New-Object System.Windows.Forms.Timer
$timer.Interval = 1500
$timer.add_Tick({
    if (-not (Get-Process -Id $AppPid -ErrorAction SilentlyContinue)) {
        $notify.Visible = $false
        $timer.Stop()
        [System.Windows.Forms.Application]::Exit()
    }
})
$timer.Start()

[System.Windows.Forms.Application]::Run()
$notify.Dispose()
''',
            encoding="utf-8",
        )

        try:
            self.tray_process = subprocess.Popen(
                [
                    "powershell.exe",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-WindowStyle",
                    "Hidden",
                    "-File",
                    str(script_path),
                    "-AppPid",
                    str(os.getpid()),
                    "-IconPath",
                    str(icon_path),
                    "-SignalPath",
                    str(self.restore_signal_path),
                    "-Tooltip",
                    self.t("tray_tip"),
                    "-ShowText",
                    self.t("tray_show"),
                    "-ExitText",
                    self.t("tray_exit"),
                ],
                creationflags=0x08000000,
            )
            self.tray_icon_added = True
        except OSError:
            self.tray_process = None
            self.tray_icon_added = False

    def _remove_tray_icon(self) -> None:
        if self.tray_process and self.tray_process.poll() is None:
            try:
                self.tray_process.terminate()
            except OSError:
                pass
        self.tray_process = None
        self.tray_icon_added = False
        self.tray_hwnd = None

    def restore_window(self) -> None:
        self.minimized_by_close = False
        self.minimized_to_taskbar = False
        if self.taskbar_proxy is not None:
            try:
                self.taskbar_proxy.deiconify()
                self._mark_taskbar_window(self.taskbar_proxy)
            except tk.TclError:
                pass
        if self.hidden:
            self.show_from_edge()
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        self._show_in_taskbar()

    def _on_taskbar_proxy_map(self, _event=None) -> None:
        if self.closing or not self.minimized_to_taskbar:
            return
        self.root.after(10, self.restore_window)

    def minimize_to_taskbar(self) -> None:
        self._cancel_hide()
        self._cancel_snap_check()
        if self.hidden:
            self.show_from_edge()
        self._save_geometry()
        self.minimized_by_close = False
        self.minimized_to_taskbar = False
        self._show_in_taskbar()
        if self.taskbar_proxy is None:
            return
        try:
            self.taskbar_proxy.deiconify()
            self._mark_taskbar_window(self.taskbar_proxy)
            self.minimized_to_taskbar = True
            self.root.withdraw()
            self.taskbar_proxy.iconify()
        except tk.TclError:
            self.minimized_to_taskbar = False
            self.restore_window()

    def minimize_to_tray(self) -> None:
        self._cancel_hide()
        self._cancel_snap_check()
        if self.hidden:
            self.show_from_edge()
        self._save_geometry()
        self.minimized_by_close = True
        self.minimized_to_taskbar = False
        self.root.withdraw()
        if self.taskbar_proxy is not None:
            try:
                self.taskbar_proxy.withdraw()
            except tk.TclError:
                pass

    def request_close(self) -> None:
        if self.close_action.get() == CLOSE_ACTION_MINIMIZE:
            self.minimize_to_tray()
        else:
            self.close()

    def _poll_restore_signal(self) -> None:
        if self.closing:
            return
        try:
            if self.restore_signal_path.exists():
                self.restore_signal_path.unlink()
                self.restore_window()
        except OSError:
            pass
        self.root.after(700, self._poll_restore_signal)

    def _apply_window_icon(self, window=None) -> None:
        target = window or self.root
        icon_path = resource_path("assets/app_icon.ico")
        png_path = resource_path("assets/app_icon_256.png")
        try:
            if icon_path.exists():
                target.iconbitmap(str(icon_path))
            if png_path.exists():
                self.app_icon_image = tk.PhotoImage(file=str(png_path))
                target.iconphoto(True, self.app_icon_image)
        except tk.TclError:
            pass

    def _load_tray_icon(self):
        icon_path = resource_path("assets/app_icon.ico")
        if sys.platform == "win32" and icon_path.exists():
            user32 = ctypes.windll.user32
            user32.LoadImageW.argtypes = [
                wintypes.HINSTANCE,
                wintypes.LPCWSTR,
                wintypes.UINT,
                ctypes.c_int,
                ctypes.c_int,
                wintypes.UINT,
            ]
            user32.LoadImageW.restype = wintypes.HICON
            IMAGE_ICON = 1
            LR_LOADFROMFILE = 0x00000010
            LR_DEFAULTSIZE = 0x00000040
            handle = user32.LoadImageW(
                None,
                str(icon_path),
                IMAGE_ICON,
                0,
                0,
                LR_LOADFROMFILE | LR_DEFAULTSIZE,
            )
            if handle:
                return handle
        ctypes.windll.user32.LoadIconW.restype = wintypes.HICON
        return ctypes.windll.user32.LoadIconW(None, IDI_APPLICATION)

    def show_settings_menu(self) -> None:
        menu = tk.Menu(self.root, tearoff=False, bg=COLOR_SURFACE, fg=COLOR_TEXT, activebackground=COLOR_SURFACE_HIGH)
        menu.add_checkbutton(
            label=self.t("settings_edge_hide"),
            variable=self.edge_hide,
            command=self._settings_changed,
        )
        menu.add_checkbutton(
            label=self.t("settings_topmost"),
            variable=self.topmost,
            command=self._topmost_changed,
        )
        menu.add_checkbutton(
            label=self.t("settings_startup"),
            variable=self.startup,
            command=self._startup_changed,
        )
        close_menu = tk.Menu(menu, tearoff=False, bg=COLOR_SURFACE, fg=COLOR_TEXT, activebackground=COLOR_SURFACE_HIGH)
        close_menu.add_radiobutton(
            label=self.t("close_action_exit"),
            value=CLOSE_ACTION_EXIT,
            variable=self.close_action,
            command=self._settings_changed,
        )
        close_menu.add_radiobutton(
            label=self.t("close_action_minimize"),
            value=CLOSE_ACTION_MINIMIZE,
            variable=self.close_action,
            command=self._settings_changed,
        )
        menu.add_cascade(label=self.t("settings_close_action"), menu=close_menu)
        language_menu = tk.Menu(menu, tearoff=False, bg=COLOR_SURFACE, fg=COLOR_TEXT, activebackground=COLOR_SURFACE_HIGH)
        for code, key in (("zh", "language_zh"), ("en", "language_en"), ("ja", "language_ja")):
            language_menu.add_radiobutton(
                label=self.t(key),
                value=code,
                variable=self.language,
                command=self._language_changed,
            )
        menu.add_cascade(label=self.t("settings_language"), menu=language_menu)
        menu.tk_popup(self.root.winfo_rootx() + 8, self.root.winfo_rooty() + 38)

    def show_help_menu(self) -> None:
        menu = tk.Menu(self.root, tearoff=False, bg=COLOR_SURFACE, fg=COLOR_TEXT, activebackground=COLOR_SURFACE_HIGH)
        menu.add_command(label=self.t("about_author"), command=self.show_about_author)
        menu.tk_popup(self.root.winfo_rootx() + 96, self.root.winfo_rooty() + 38)

    def open_github(self) -> None:
        webbrowser.open_new_tab(GITHUB_URL)

    def show_about_author(self) -> None:
        about = tk.Toplevel(self.root)
        about.title(self.t("about_author"))
        about.configure(bg=COLOR_BG)
        about.resizable(False, False)
        about.transient(self.root)
        about.attributes("-topmost", bool(self.topmost.get()))

        tk.Label(
            about,
            text=f"{APP_TITLE} / {APP_ENGLISH_NAME}",
            bg=COLOR_BG,
            fg=COLOR_TEXT,
            font=self.font_big,
        ).pack(padx=24, pady=(20, 8))
        tk.Label(
            about,
            text=f"{self.t('author')}：{AUTHOR}\n{self.t('wechat')}：{WECHAT}",
            bg=COLOR_BG,
            fg=COLOR_TEXT,
            font=self.font_ui,
            justify="center",
        ).pack(padx=24, pady=(0, 14))

        image_path = resource_path("assets/lxfs.png")
        if image_path.exists():
            about.qr_image = tk.PhotoImage(file=str(image_path))
            tk.Label(about, image=about.qr_image, bg=COLOR_BG).pack(padx=24, pady=(0, 18))
        else:
            tk.Label(
                about,
                text=self.t("qr_missing"),
                bg=COLOR_BG,
                fg=COLOR_MUTED,
                font=self.font_ui,
            ).pack(padx=24, pady=(0, 18))

        tk.Button(
            about,
            text=self.t("close"),
            bg=COLOR_PRIMARY,
            fg=COLOR_ON_PRIMARY,
            activebackground=COLOR_PRIMARY_HOVER,
            activeforeground=COLOR_ON_PRIMARY,
            relief="flat",
            command=about.destroy,
        ).pack(ipadx=18, ipady=4, pady=(0, 20))

        about.update_idletasks()
        x = self.root.winfo_x() + max(0, (self.root.winfo_width() - about.winfo_width()) // 2)
        y = self.root.winfo_y() + 64
        about.geometry(f"+{x}+{y}")

    def show_archive(self) -> None:
        archive = tk.Toplevel(self.root)
        archive.title(self.t("archive"))
        archive.configure(bg=COLOR_BG)
        archive.minsize(320, 420)
        archive.transient(self.root)
        archive.attributes("-topmost", bool(self.topmost.get()))

        tk.Label(
            archive,
            text=self.t("archive_title"),
            bg=COLOR_BG,
            fg=COLOR_TEXT,
            font=self.font_title,
        ).pack(fill="x", padx=18, pady=(16, 8))

        body = tk.Frame(archive, bg=COLOR_BG)
        body.pack(fill="both", expand=True, padx=14, pady=(0, 12))

        archived_items = [item for item in self.store.items if item.get("done")]
        if not archived_items:
            tk.Label(
                body,
                text=self.t("archive_empty"),
                bg=COLOR_BG,
                fg=COLOR_MUTED,
                font=self.font_ui,
            ).pack(fill="both", expand=True, pady=48)
        else:
            for item in archived_items:
                row = tk.Frame(body, bg=COLOR_SURFACE, highlightbackground=COLOR_OUTLINE, highlightthickness=1)
                row.pack(fill="x", pady=4)
                tk.Label(
                    row,
                    text=item.get("text", ""),
                    bg=COLOR_SURFACE,
                    fg=COLOR_TEXT,
                    anchor="w",
                    justify="left",
                    wraplength=240,
                    font=self.font_ui,
                ).pack(side="left", fill="x", expand=True, padx=10, pady=9)
                tk.Button(
                    row,
                    text=self.t("restore"),
                    bg=COLOR_SURFACE,
                    fg=COLOR_PRIMARY,
                    activebackground=COLOR_SURFACE_HIGH,
                    relief="flat",
                    command=lambda item_id=item["id"], window=archive: self.restore_archived_item(item_id, window),
                ).pack(side="right", padx=(0, 4), pady=6)
                tk.Button(
                    row,
                    text="×",
                    width=3,
                    bg=COLOR_SURFACE,
                    fg=COLOR_ERROR,
                    activebackground=COLOR_ERROR_CONTAINER,
                    relief="flat",
                    command=lambda item_id=item["id"], window=archive: self.delete_archived_item(item_id, window),
                ).pack(side="right", padx=(0, 6), pady=6)

        actions = tk.Frame(archive, bg=COLOR_BG)
        actions.pack(fill="x", padx=14, pady=(0, 16))
        if archived_items:
            tk.Button(
                actions,
                text=self.t("clear_archive"),
                bg=COLOR_ERROR_CONTAINER,
                fg=COLOR_ERROR,
                activebackground=COLOR_ERROR_HOVER,
                relief="flat",
                font=self.font_tool,
                command=lambda window=archive: self.clear_archive(window),
            ).pack(side="left", ipadx=12, ipady=5)
        tk.Button(
            actions,
            text=self.t("close"),
            bg=COLOR_PRIMARY,
            fg=COLOR_ON_PRIMARY,
            activebackground=COLOR_PRIMARY_HOVER,
            activeforeground=COLOR_ON_PRIMARY,
            relief="flat",
            font=self.font_tool,
            command=archive.destroy,
        ).pack(side="right", ipadx=18, ipady=5)

        archive.update_idletasks()
        x = self.root.winfo_x() + max(0, (self.root.winfo_width() - archive.winfo_width()) // 2)
        y = self.root.winfo_y() + 64
        archive.geometry(f"+{x}+{y}")

    def restore_archived_item(self, item_id: str, archive_window: tk.Toplevel) -> None:
        for item in self.store.items:
            if item["id"] == item_id:
                item["done"] = False
                break
        self.store.save()
        self.render_items()
        archive_window.destroy()
        self.show_archive()

    def delete_archived_item(self, item_id: str, archive_window: tk.Toplevel) -> None:
        self.store.items = [item for item in self.store.items if item["id"] != item_id]
        self.store.save()
        archive_window.destroy()
        self.show_archive()

    def clear_archive(self, archive_window: tk.Toplevel) -> None:
        if not messagebox.askyesno(
            self.t("clear_archive_confirm_title"),
            self.t("clear_archive_confirm"),
            parent=archive_window,
        ):
            return
        self.store.items = [item for item in self.store.items if not item.get("done")]
        self.store.save()
        self.render_items()
        archive_window.destroy()
        self.show_archive()

    def render_groups(self) -> None:
        for child in self.sidebar_frame.winfo_children():
            child.destroy()

        self._group_button(self.sidebar_frame, ALL_GROUPS_ID, self.t("all_todos")).pack(fill="x", padx=8, pady=(10, 5))

        for group in self.store.groups:
            row = tk.Frame(self.sidebar_frame, bg=COLOR_SURFACE_CONTAINER)
            row.pack(fill="x", padx=8, pady=3)
            self._group_button(row, group["id"], self.group_name(group["id"])).pack(side="left", fill="x", expand=True)
            if group["id"] != DEFAULT_GROUP_ID:
                tk.Button(
                    row,
                    text="×",
                    width=2,
                    bg=COLOR_SURFACE_CONTAINER,
                    fg=COLOR_ERROR,
                    activebackground=COLOR_ERROR_CONTAINER,
                    relief="flat",
                    bd=0,
                    highlightthickness=0,
                    font=self.font_tool,
                    cursor="hand2",
                    command=lambda group_id=group["id"]: self.delete_group(group_id),
                ).pack(side="right", padx=(3, 0))

        tk.Button(
            self.sidebar_frame,
            text=f"+ {self.t('new_group')}",
            bg=COLOR_SURFACE_CONTAINER,
            fg=COLOR_PRIMARY,
            activebackground=COLOR_SURFACE_HIGH,
            relief="flat",
            bd=0,
            highlightthickness=0,
            font=self.font_tool,
            padx=8,
            pady=5,
            anchor="w",
            command=self.add_group,
        ).pack(fill="x", padx=8, pady=(10, 4))

    def _group_button(self, parent, group_id: str, text: str) -> tk.Button:
        selected = self.selected_group_id == group_id
        return tk.Button(
            parent,
            text=text,
            bg=COLOR_PRIMARY if selected else COLOR_SURFACE_CONTAINER,
            fg=COLOR_ON_PRIMARY if selected else COLOR_TEXT,
            activebackground=COLOR_PRIMARY_HOVER if selected else COLOR_SURFACE_HIGH,
            activeforeground=COLOR_ON_PRIMARY if selected else COLOR_TEXT,
            relief="flat",
            bd=0,
            highlightthickness=0,
            anchor="w",
            padx=8,
            pady=6,
            wraplength=88,
            font=self.font_tool if selected else self.font_small,
            cursor="hand2",
            command=lambda: self.select_group(group_id),
        )

    def select_group(self, group_id: str) -> None:
        self.selected_group_id = group_id
        self.store.settings["selected_group_id"] = group_id
        self.store.save()
        self.render_groups()
        self.render_items()

    def add_group(self) -> None:
        name = simpledialog.askstring(self.t("new_group"), self.t("new_group_prompt"), parent=self.root)
        if not name:
            return
        group = {"id": self.store.new_id(), "name": name.strip()}
        if not group["name"]:
            return
        self.store.groups.append(group)
        self.selected_group_id = group["id"]
        self.store.settings["selected_group_id"] = group["id"]
        self.store.save()
        self.render_groups()
        self.render_items()

    def delete_group(self, group_id: str) -> None:
        if group_id == DEFAULT_GROUP_ID:
            return
        group_name = self.group_name(group_id)
        if not messagebox.askyesno(
            self.t("delete_group_confirm_title"),
            self.t("delete_group_confirm", group=group_name),
            parent=self.root,
        ):
            return
        self.store.groups = [group for group in self.store.groups if group["id"] != group_id]
        for item in self.store.items:
            if item.get("group_id") == group_id:
                item["group_id"] = DEFAULT_GROUP_ID
        if self.selected_group_id == group_id:
            self.selected_group_id = ALL_GROUPS_ID
            self.store.settings["selected_group_id"] = ALL_GROUPS_ID
        self.store.save()
        self.render_groups()
        self.render_items()

    def _restore_geometry(self) -> None:
        width = max(MIN_WIDTH, int(self.store.settings.get("width", DEFAULT_WIDTH)))
        height = max(MIN_HEIGHT, int(self.store.settings.get("height", DEFAULT_HEIGHT)))
        x = int(self.store.settings.get("x", 80))
        y = int(self.store.settings.get("y", 80))
        left, top, right, bottom = work_area(self.root)
        x = clamp(x, left, max(left, right - width))
        y = clamp(y, top, max(top, bottom - height))
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _resize_list(self, event) -> None:
        self.canvas.itemconfigure(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event) -> None:
        if self.root.focus_get() is not None:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _add_resize_handles(self) -> None:
        handles = [
            ("right", {"relx": 1, "rely": 0, "relheight": 1, "width": 6, "anchor": "ne"}, "sb_h_double_arrow"),
            ("bottom", {"relx": 0, "rely": 1, "relwidth": 1, "height": 6, "anchor": "sw"}, "sb_v_double_arrow"),
            ("bottom_right", {"relx": 1, "rely": 1, "width": 16, "height": 16, "anchor": "se"}, "bottom_right_corner"),
        ]
        for edge, place_args, cursor in handles:
            handle = tk.Frame(self.root, bg=COLOR_OUTLINE, cursor=cursor)
            handle.place(**place_args)
            handle.bind("<ButtonPress-1>", lambda event, resize_edge=edge: self._start_resize(event, resize_edge))
            handle.bind("<B1-Motion>", self._resize)
            handle.bind("<ButtonRelease-1>", self._end_drag)

    def _apply_topmost(self) -> None:
        self.root.attributes("-topmost", bool(self.topmost.get()))

    def _topmost_changed(self) -> None:
        self.store.settings["topmost_explicit"] = True
        self._apply_topmost()
        self._settings_changed()

    def _startup_changed(self) -> None:
        try:
            Startup.set_enabled(bool(self.startup.get()))
        except OSError as exc:
            self.startup.set(Startup.is_enabled())
            messagebox.showerror(
                self.t("startup_error_title"),
                self.t("startup_error", error=exc),
            )

    def _settings_changed(self) -> None:
        self.store.settings["edge_hide"] = bool(self.edge_hide.get())
        self.store.settings["topmost"] = bool(self.topmost.get())
        if self.store.settings.get("topmost_explicit"):
            self.store.settings["topmost_explicit"] = True
        self.store.settings["language"] = self.language.get()
        self.store.settings["close_action"] = self.close_action.get()
        self.store.save()

    def _language_changed(self) -> None:
        self.store.settings["language"] = self.language.get()
        self.store.save()
        self.rebuild_ui()
        self._remove_tray_icon()
        self.root.after(250, self._create_tray_icon)

    def rebuild_ui(self) -> None:
        for child in self.root.winfo_children():
            child.destroy()
        self._build()

    def _start_drag(self, event) -> None:
        self._cancel_hide()
        self._cancel_animation()
        self._cancel_snap_check()
        self.dragging = True
        self.hidden = False
        self.snapped_edge = None
        self.drag_offset = (event.x_root - self.root.winfo_x(), event.y_root - self.root.winfo_y())

    def _drag(self, event) -> None:
        x = event.x_root - self.drag_offset[0]
        y = event.y_root - self.drag_offset[1]
        self.root.geometry(f"+{x}+{y}")

    def _end_drag(self, _event=None) -> None:
        self.dragging = False
        self.resize_start = None
        self._save_geometry()
        if self.edge_hide.get():
            self.snap_if_near_edge()

    def _start_resize(self, event, edge: str = "bottom_right") -> None:
        self._cancel_hide()
        self._cancel_animation()
        self._cancel_snap_check()
        self.dragging = False
        self.hidden = False
        self.snapped_edge = None
        self.resize_start = (
            event.x_root,
            event.y_root,
            self.root.winfo_width(),
            self.root.winfo_height(),
            self.root.winfo_x(),
            self.root.winfo_y(),
            edge,
        )

    def _resize(self, event) -> None:
        if not self.resize_start:
            return
        start_x, start_y, start_w, start_h, window_x, window_y, edge = self.resize_start
        delta_x = event.x_root - start_x
        delta_y = event.y_root - start_y
        width = start_w
        height = start_h

        if edge in ("right", "bottom_right"):
            width = max(MIN_WIDTH, start_w + delta_x)
        if edge in ("bottom", "bottom_right"):
            height = max(MIN_HEIGHT, start_h + delta_y)

        self.root.geometry(f"{width}x{height}+{window_x}+{window_y}")

    def _save_geometry(self) -> None:
        if self.hidden:
            self.store.settings["snapped_edge"] = self.snapped_edge
            self.store.save()
            return

        x, y, rect_right, rect_bottom = window_rect(self.root)
        self.store.settings.update(
            {
                "x": x,
                "y": y,
                "width": max(MIN_WIDTH, rect_right - x),
                "height": max(MIN_HEIGHT, rect_bottom - y),
                "snapped_edge": self.snapped_edge,
            }
        )
        self.store.save()

    def _on_enter(self, _event=None) -> None:
        self._cancel_hide()
        if self.hidden:
            if self.edge_reveal_ready:
                self.show_from_edge()
            return

    def _on_configure(self, _event=None) -> None:
        if self.restoring_from_zoom:
            return
        try:
            state = self.root.state()
        except tk.TclError:
            return

        if state == "zoomed":
            self.restoring_from_zoom = True
            if self.last_normal_geometry:
                self.root.state("normal")
                self.root.geometry(self.last_normal_geometry)
            else:
                self.root.state("normal")
            self.restoring_from_zoom = False
            return

        if state == "normal" and not self.hidden and not self.animation_after_id:
            self.last_normal_geometry = (
                f"{self.root.winfo_width()}x{self.root.winfo_height()}"
                f"+{self.root.winfo_x()}+{self.root.winfo_y()}"
            )

    def _schedule_snap_check(self) -> None:
        if (
            not self.edge_hide.get()
            or self.hidden
            or self.animation_after_id
            or self.programmatic_move
            or self.dragging
            or self.resize_start
        ):
            return
        if self.snap_after_id:
            self.root.after_cancel(self.snap_after_id)
        self.snap_after_id = self.root.after(260, self._snap_after_window_move)

    def _snap_after_window_move(self) -> None:
        self.snap_after_id = None
        if not self.edge_hide.get() or self.hidden or self.animation_after_id or self.programmatic_move:
            return
        if self.snapped_edge in VALID_SNAP_EDGES and self.is_attached_to_edge():
            return
        edge = self.edge_if_near()
        if edge:
            self.snap_to_edge(edge, auto_hide=True)

    def _on_leave(self, _event=None) -> None:
        if self.hidden:
            self.edge_reveal_ready = True
            return
        if self.edge_hide.get() and self.is_attached_to_edge():
            self._cancel_hide()
            self.hide_after_id = self.root.after(HIDE_DELAY_MS, self._hide_if_pointer_left)

    def _hide_if_pointer_left(self) -> None:
        self.hide_after_id = None
        if not self.edge_hide.get() or not self.is_attached_to_edge():
            return

        pointer_x = self.root.winfo_pointerx()
        pointer_y = self.root.winfo_pointery()
        x, y, rect_right, rect_bottom = window_rect(self.root)
        width = rect_right - x
        height = rect_bottom - y
        left, top, right, _bottom = work_area(self.root)
        inside_window = x <= pointer_x <= x + width and y <= pointer_y <= y + height
        in_top_hot_zone = (
            self.snapped_edge == "top"
            and top <= pointer_y <= top + TOP_HOT_ZONE
            and x - TOP_POP_MARGIN <= pointer_x <= x + width + TOP_POP_MARGIN
        )
        in_left_hot_zone = self.snapped_edge == "left" and left <= pointer_x <= left + TOP_HOT_ZONE
        in_right_hot_zone = self.snapped_edge == "right" and right - TOP_HOT_ZONE <= pointer_x <= right

        if inside_window or in_top_hot_zone or in_left_hot_zone or in_right_hot_zone:
            return
        self.hide_to_edge()

    def _hide_after_snap(self) -> None:
        self.hide_after_id = None
        self.hide_to_edge()

    def _enable_edge_reveal_when_clear(self) -> None:
        if not self.hidden:
            self.edge_reveal_ready = True
            return
        if self._pointer_in_reveal_zone():
            self.root.after(200, self._enable_edge_reveal_when_clear)
            return
        self.edge_reveal_ready = True

    def _pointer_in_reveal_zone(self) -> bool:
        if self.snapped_edge not in VALID_SNAP_EDGES:
            return False

        pointer_x = self.root.winfo_pointerx()
        pointer_y = self.root.winfo_pointery()
        x, y, rect_right, rect_bottom = window_rect(self.root)
        left, top, right, _bottom = work_area(self.root)

        if self.snapped_edge == "top":
            return (
                top <= pointer_y <= top + TOP_HOT_ZONE
                and x - TOP_POP_MARGIN <= pointer_x <= rect_right + TOP_POP_MARGIN
            )
        if self.snapped_edge == "left":
            return (
                left <= pointer_x <= left + TOP_HOT_ZONE
                and y - TOP_POP_MARGIN <= pointer_y <= rect_bottom + TOP_POP_MARGIN
            )
        if self.snapped_edge == "right":
            return (
                right - TOP_HOT_ZONE <= pointer_x <= right
                and y - TOP_POP_MARGIN <= pointer_y <= rect_bottom + TOP_POP_MARGIN
            )
        return False

    def _cancel_hide(self) -> None:
        if self.hide_after_id:
            self.root.after_cancel(self.hide_after_id)
            self.hide_after_id = None

    def _cancel_animation(self) -> None:
        if self.animation_after_id:
            self.root.after_cancel(self.animation_after_id)
            self.animation_after_id = None

    def _cancel_snap_check(self) -> None:
        if self.snap_after_id:
            self.root.after_cancel(self.snap_after_id)
            self.snap_after_id = None

    def _move_window(self, x: int, y: int, animate: bool = True, on_done=None) -> None:
        self._cancel_animation()
        self._place_window(x, y)
        if on_done:
            self.root.after(30, on_done)

    def _place_window(self, x: int, y: int) -> None:
        self.programmatic_move = True
        self.root.geometry(f"+{int(x)}+{int(y)}")
        self.root.after(30, self._finish_programmatic_move)

    def _finish_programmatic_move(self) -> None:
        self.programmatic_move = False

    def _maybe_hide_after_start(self) -> None:
        if self.edge_hide.get() and self.is_attached_to_edge():
            self.hide_to_edge()

    def _poll_top_autohide(self) -> None:
        if self.edge_hide.get() and self.snapped_edge == "top" and self.hidden and not self.animation_after_id:
            pointer_in_zone = self._pointer_in_reveal_zone()
            if pointer_in_zone and self.edge_reveal_ready:
                self._cancel_hide()
                self.show_from_edge()
            elif not pointer_in_zone:
                self.edge_reveal_ready = True

        self.root.after(120, self._poll_top_autohide)

    def nearest_edge(self) -> str:
        left, top, right, _bottom = work_area(self.root)
        x, y, rect_right, _rect_bottom = window_rect(self.root)
        width = rect_right - x
        distances = {
            "left": abs(x - left),
            "right": abs((x + width) - right),
            "top": abs(y - top),
        }
        return min(distances, key=distances.get)

    def edge_if_near(self) -> str | None:
        left, top, right, _bottom = work_area(self.root)
        x, y, rect_right, _rect_bottom = window_rect(self.root)
        width = rect_right - x
        if x <= left + EDGE_THRESHOLD:
            return "left"
        if x + width >= right - EDGE_THRESHOLD:
            return "right"
        if y <= top + EDGE_THRESHOLD:
            return "top"
        return None

    def is_attached_to_edge(self) -> bool:
        if self.snapped_edge not in VALID_SNAP_EDGES or self.hidden:
            return False

        left, top, right, _bottom = work_area(self.root)
        x, y, rect_right, _rect_bottom = window_rect(self.root)
        width = rect_right - x

        if self.snapped_edge == "left":
            return abs(x - left) <= EDGE_THRESHOLD
        if self.snapped_edge == "right":
            return abs((x + width) - right) <= EDGE_THRESHOLD
        if self.snapped_edge == "top":
            return abs(y - top) <= EDGE_THRESHOLD
        return False

    def snap_if_near_edge(self) -> None:
        edge = self.edge_if_near()
        if edge:
            self.snap_to_edge(edge, auto_hide=True)
        else:
            self.snapped_edge = None
            self._save_geometry()

    def snap_to_edge(self, edge: str, auto_hide: bool = False, hide_delay_ms: int = AUTO_HIDE_AFTER_SNAP_MS) -> None:
        if edge not in VALID_SNAP_EDGES:
            self.snapped_edge = None
            self._save_geometry()
            return

        left, top, right, bottom = work_area(self.root)
        x, y, rect_right, rect_bottom = window_rect(self.root)
        width = rect_right - x
        height = rect_bottom - y

        if edge == "left":
            x = left
            y = clamp(y, top, bottom - height)
        elif edge == "right":
            x = right - width
            y = clamp(y, top, bottom - height)
        elif edge == "top":
            y = top
            x = clamp(x, left, right - width)

        self.snapped_edge = edge
        self.hidden = False
        self.edge_reveal_ready = True
        def after_snap() -> None:
            self._save_geometry()
            if auto_hide and self.edge_hide.get():
                self._cancel_hide()
                if hide_delay_ms <= 0:
                    self._hide_after_snap()
                else:
                    self.hide_after_id = self.root.after(hide_delay_ms, self._hide_after_snap)

        self._move_window(x, y, on_done=after_snap)

    def hide_to_nearest_edge(self) -> None:
        self.snap_to_edge(self.nearest_edge(), auto_hide=True, hide_delay_ms=0)

    def hide_to_edge(self) -> None:
        if self.hidden:
            return
        if not self.edge_hide.get():
            return
        if self.snapped_edge not in VALID_SNAP_EDGES:
            return
        if not self.is_attached_to_edge():
            return

        left, top, right, bottom = work_area(self.root)
        x, y, rect_right, rect_bottom = window_rect(self.root)
        width = rect_right - x
        height = rect_bottom - y

        if self.snapped_edge == "left":
            x = left - width + EDGE_STRIP
        elif self.snapped_edge == "right":
            x = right - EDGE_STRIP
        elif self.snapped_edge == "top":
            y = top - height + TOP_EDGE_STRIP

        self.hidden = True
        self.edge_reveal_ready = False
        self._move_window(x, y)
        self.root.after(400, self._enable_edge_reveal_when_clear)

    def show_from_edge(self) -> None:
        left, top, right, bottom = work_area(self.root)
        x, y, rect_right, rect_bottom = window_rect(self.root)
        width = rect_right - x
        height = rect_bottom - y

        if self.snapped_edge == "left":
            x = left
            y = clamp(y, top, bottom - height)
        elif self.snapped_edge == "right":
            x = right - width
            y = clamp(y, top, bottom - height)
        elif self.snapped_edge == "top":
            y = top
            x = clamp(x, left, right - width)

        self.hidden = False
        self.edge_reveal_ready = True
        self._move_window(x, y, on_done=self._save_geometry)

    def add_item(self) -> None:
        text = self.new_text.get().strip()
        if not text:
            return
        group_id = self.selected_group_id
        if group_id == ALL_GROUPS_ID or not any(group["id"] == group_id for group in self.store.groups):
            group_id = self.store.groups[0]["id"]
        self.store.items.insert(
            0,
            {
                "id": self.store.new_id(),
                "text": text,
                "done": False,
                "group_id": group_id,
                "created_at": Store.now_iso(),
            },
        )
        self.new_text.set("")
        self.store.save()
        self.render_groups()
        self.render_items()

    def toggle_item(self, item_id: str, value: bool) -> None:
        for item in self.store.items:
            if item["id"] == item_id:
                item["done"] = value
                break
        self.store.save()
        self.render_items()

    def delete_item(self, item_id: str) -> None:
        self.store.items = [item for item in self.store.items if item["id"] != item_id]
        self.store.save()
        self.render_items()

    def clear_done(self) -> None:
        self.store.items = [item for item in self.store.items if not item.get("done")]
        self.store.save()
        self.render_items()

    def render_items(self) -> None:
        for child in self.list_frame.winfo_children():
            child.destroy()

        all_active_items = [item for item in self.store.items if not item.get("done")]
        if self.selected_group_id == ALL_GROUPS_ID:
            active_items = all_active_items
        else:
            active_items = [
                item for item in all_active_items if item.get("group_id") == self.selected_group_id
            ]
        archived_count = len([item for item in self.store.items if item.get("done")])
        open_count = len(active_items)
        summary = tk.Frame(self.list_frame, bg=COLOR_BG)
        summary.pack(fill="x", pady=(0, 8))
        tk.Label(
            summary,
            text=self.t("todo_summary", open=open_count, archived=archived_count),
            bg=COLOR_BG,
            fg=COLOR_MUTED,
            font=self.font_small,
        ).pack(side="left")

        if not active_items:
            tk.Label(
                self.list_frame,
                text=self.t("empty"),
                bg=COLOR_BG,
                fg=COLOR_MUTED,
                font=self.font_ui,
            ).pack(fill="x", pady=40)
            return

        for item in active_items:
            row = tk.Frame(self.list_frame, bg=COLOR_SURFACE, highlightbackground=COLOR_OUTLINE, highlightthickness=1)
            row.pack(fill="x", pady=6)
            row.grid_columnconfigure(1, weight=1)

            done_var = tk.BooleanVar(value=bool(item.get("done")))
            check = tk.Checkbutton(
                row,
                variable=done_var,
                command=lambda item_id=item["id"], var=done_var: self.toggle_item(item_id, var.get()),
                bg=COLOR_SURFACE,
                activebackground=COLOR_SURFACE,
                selectcolor=COLOR_SURFACE_HIGH,
            )
            check.grid(row=0, column=0, sticky="n", padx=(10, 4), pady=12)

            fg = COLOR_MUTED if item.get("done") else COLOR_TEXT
            item_font = self.font_done if item.get("done") else self.font_ui
            body = tk.Frame(row, bg=COLOR_SURFACE)
            body.grid(row=0, column=1, sticky="ew", pady=10)
            label = tk.Label(
                body,
                text=item.get("text", ""),
                bg=COLOR_SURFACE,
                fg=fg,
                anchor="w",
                justify="left",
                wraplength=max(170, self.root.winfo_width() - 280),
                font=item_font,
            )
            label.pack(fill="x")

            meta = tk.Frame(body, bg=COLOR_SURFACE)
            meta.pack(fill="x", pady=(4, 0))
            tk.Label(
                meta,
                text=self.t("created_at", time=self.format_created_at(str(item.get("created_at") or ""))),
                bg=COLOR_SURFACE,
                fg=COLOR_MUTED,
                anchor="w",
                font=self.font_small,
            ).pack(side="left", fill="x", expand=True)
            tk.Label(
                meta,
                text=self.group_name(str(item.get("group_id") or DEFAULT_GROUP_ID)),
                bg=COLOR_SURFACE,
                fg=COLOR_MUTED,
                anchor="e",
                font=self.font_small,
            ).pack(side="right")

            delete = tk.Button(
                row,
                text="×",
                width=3,
                bg=COLOR_SURFACE,
                fg=COLOR_ERROR,
                activebackground=COLOR_ERROR_CONTAINER,
                relief="flat",
                bd=0,
                highlightthickness=0,
                font=self.font_tool,
                cursor="hand2",
                command=lambda item_id=item["id"]: self.delete_item(item_id),
            )
            delete.grid(row=0, column=2, sticky="n", padx=(8, 10), pady=9)

    def close(self) -> None:
        self.closing = True
        self._cancel_snap_check()
        self._cancel_animation()
        self._remove_tray_icon()
        self._save_geometry()
        if self.taskbar_proxy is not None:
            try:
                self.taskbar_proxy.destroy()
            except tk.TclError:
                pass
            self.taskbar_proxy = None
        self.root.destroy()

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    if sys.platform != "win32":
        language = Store().settings.get("language", "zh")
        messagebox.showwarning(APP_TITLE, LANGUAGES.get(language, LANGUAGES["zh"])["system_windows_only"])
    TodoApp().run()


if __name__ == "__main__":
    main()
