# 🚀 JASS Future Launcher

A futuristic PySide6 desktop launcher for a personal collection of applications stored in **Downloads** and its subfolders.

## What it does

Open one launcher and click **▶ Launch** on any discovered application. The launcher recursively scans:

```text
C:\Users\<YourName>\Downloads\
```

It is especially useful when many small PySide6 projects live in separate folders.

## Supported files

- `.py`
- `.pyw`
- `.exe`
- `.bat`
- `.cmd`
- `.lnk`

Python files are launched with the Windows `py` launcher when available, with the application's own folder as the working directory. This mirrors the normal PowerShell workflow such as `py my_app.py`.

## Global Python / PySide6 Environment

This launcher intentionally **does not require a separate virtual environment**.

It assumes common requirements such as PySide6 are installed globally and
launches Python applications through the Windows Python launcher:

```powershell
py MyApplication.py
```

The launcher does not create, activate, modify, or manage `.venv` directories.

Application cards identify the runtime:

- 🐍 **GLOBAL PYTHON** — `.py` / `.pyw`
- 🪟 **WINDOWS APP** — `.exe`, `.bat`, `.cmd`, `.lnk`

This keeps the launcher lightweight and matches a personal collection of
small PySide6 utilities sharing one global Python environment.

## Features

- 🔎 Search by application name/path/category
- 🗂️ Recursive Downloads scanning
- 🚀 One-click launch
- ⭐ Favorites
- 🧩 Automatic categories
- ➕ Add applications manually
- 📁 Open containing folder
- ↻ Rescan
- 🌌 Futuristic dark UI
- 💾 Persistent configuration

Common dependency/development folders are ignored (`venv`, `.venv`, `.git`, `node_modules`, `__pycache__`, etc.) so the launcher does not become cluttered with thousands of files.

## Run

```powershell
py -m pip install PySide6
py Jass_Future_Launcher.py
```

## Configuration

The launcher stores its small configuration database at:

```text
%APPDATA%\JassFutureLauncher\apps.json
```

Your applications are not moved or modified.

## Typical workflow

```text
Create PySide6 app
        ↓
Save project under Downloads
        ↓
Open JASS Future Launcher
        ↓
Click ↻ Scan
        ↓
Application appears
        ↓
Click ▶ Launch
```

## Future roadmap

Possible additions without changing the launcher concept:

- Custom icons
- Drag-and-drop registration
- Custom categories/tags
- Recently launched apps
- Most-used apps
- Pin to top
- Keyboard shortcuts
- Quick command palette
- Per-app Python interpreter
- Per-app command-line arguments
- Environment profiles
- Import/export launcher database
- Windows startup option
- Optional custom themes/wallpapers

## Design principle

> **Find it → click it → launch it.**

The launcher should remain a lightweight personal application hub rather than becoming another IDE.
