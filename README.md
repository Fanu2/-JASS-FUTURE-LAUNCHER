
<img width="1850" height="975" alt="image" src="https://github.com/user-attachments/assets/87959169-fda2-469f-9d76-eba0d3fad31a" />

# 🚀 JASS Future Launcher

A futuristic **PySide6 desktop application launcher** for managing and launching a growing personal collection of Python, PySide6, and Windows applications stored in the `Downloads` folder and its subfolders.

> **Find it → Click it → Launch it.**

Instead of searching through multiple project folders and remembering where every application lives, JASS Future Launcher provides one central dashboard.

---

## ✨ Features

- 🚀 One-click application launching
- 🔎 Search applications
- 🗂️ Automatic category detection
- ⭐ Favorites
- ➕ Add applications manually
- 📁 Open application folder
- ↻ Rescan Downloads
- 🌌 Futuristic dark interface
- 📱 Scrollable application grid
- 💾 Persistent launcher configuration
- 🐍 Global Python/PySide6 support
- 🪟 Windows application support

---

## 📂 Automatic Application Discovery

On startup, the launcher recursively scans:

```text
C:\Users\<YourName>\Downloads\
```

including its subfolders.

Supported application files:

```text
.py
.pyw
.exe
.bat
.cmd
.lnk
```

For example:

```text
Downloads
│
├── Mizo_Love
│   └── Mizo_Love.py
│
├── Grammar_Memory_Lab
│   └── grammar_memory_lab.py
│
├── Jass_Subtitle_Studio
│   └── Jass_Subtitle_Studio.py
│
└── Shorts_Studio
    └── shorts_studio.py
```

These applications can be discovered and launched from the dashboard.

---

# 🐍 Global Python / PySide6 Environment

This project intentionally **does not require a separate virtual environment**.

It is designed for a Windows setup where common Python requirements such as:

```text
Python
PySide6
Pillow
other commonly used packages
```

are installed globally.

Python applications are launched through the Windows Python launcher:

```powershell
py .\your_application.py
```

The launcher does **not**:

- create `.venv`
- activate `.venv`
- manage virtual environments
- install dependencies
- modify individual projects

This keeps the launcher lightweight and matches a personal collection of small
PySide6 applications sharing one global Python environment.

---

# 🐍 Python vs Windows Applications

Application cards identify the runtime.

### Python applications

```text
🐍 GLOBAL PYTHON
```

Used for:

```text
.py
.pyw
```

They are launched using:

```powershell
py application.py
```

### Windows applications

```text
🪟 WINDOWS APP
```

Used for:

```text
.exe
.bat
.cmd
.lnk
```

These are launched directly through Windows.

---

# ▶️ Running the Launcher

Open PowerShell and go to the Downloads folder:

```powershell
cd "C:\Users\singh\Downloads"
```

Then run:

```powershell
py .\Jass_Future_Launcher_Global_Python.py
```

### Important PowerShell detail

Do not simply type:

```powershell
Jass_Future_Launcher_Global_Python.py
```

PowerShell does not automatically execute files from the current directory.

Use:

```powershell
py .\Jass_Future_Launcher_Global_Python.py
```

This also ensures that the application uses your Python installation.

---

# 📦 Installation

If PySide6 is already installed globally, no additional installation is required.

Otherwise:

```powershell
py -m pip install PySide6
```

Then:

```powershell
py .\Jass_Future_Launcher_Global_Python.py
```

---

# ⭐ Favorites

Frequently used applications can be marked as favorites.

```text
☆
```

becomes:

```text
★
```

Favorites can then be displayed separately.

---

# 🔎 Search

Use the search box to quickly locate applications.

Search can match:

- application name
- category
- file path

Examples:

```text
mizo
```

```text
subtitle
```

```text
grammar
```

```text
ai
```

---

# 🗂️ Automatic Categories

The launcher attempts to classify applications based on their names.

Possible categories include:

```text
🤖 AI
🎬 MEDIA
🌐 LANGUAGE
🧰 TOOLS
💻 DEVELOPMENT
📚 DOCUMENTS
🏛️ REVENUE
🚀 OTHER
```

The classification system is deliberately lightweight and can be expanded later.

---

# ➕ Add Application

Applications outside the Downloads tree can be added manually using:

```text
＋ Add App
```

The launcher remembers manually added applications.

---

# 📁 Open Application Folder

Each application provides an option to open its containing folder.

Useful when you want to:

- inspect the project
- edit the Python source
- access assets
- open documentation
- modify the application

---

# ↻ Rescan

When a new PySide6 application is created in Downloads, click:

```text
↻ Scan
```

The launcher searches Downloads again and discovers newly added applications.

---

# 💾 Configuration

Launcher configuration is stored under:

```text
%APPDATA%\JassFutureLauncher\
```

The main configuration file is:

```text
apps.json
```

It stores information such as:

```text
application path
application name
category
favorite status
last launch time
manual registration
```

Your actual application files are **not moved or modified**.

---

# 🛡️ Dependency Directory Filtering

The scanner ignores common development and dependency directories:

```text
.git
.venv
venv
env
__pycache__
node_modules
.pytest_cache
.mypy_cache
.vscode
site-packages
```

This prevents the launcher from displaying thousands of dependency files.

The objective is to discover **applications**, not every Python file.

---

# 🏗️ Typical Workflow

```text
Create PySide6 application
          ↓
Put project in Downloads
          ↓
Run JASS Future Launcher
          ↓
Launcher scans Downloads
          ↓
Application appears
          ↓
Click ▶ Launch
```

No shortcut creation is required.

No separate launcher configuration is required.

No virtual environment is required.

---

# 🎯 Project Philosophy

JASS Future Launcher is intentionally simple.

Its primary purpose is:

> **Find it → Click it → Launch it.**

It should remain a personal application hub rather than becoming another IDE.

Individual projects remain independent.

---

# 🚀 Future Roadmap

The current version provides a foundation for a more powerful personal software dashboard.

Possible future additions:

## Application Management

- Custom application icons
- Custom names
- Descriptions
- Tags
- Custom categories
- Pin applications
- Recently launched applications
- Most-used applications
- Launch history

## Python Controls

- Per-application Python interpreter
- Command-line arguments
- Working-directory settings
- Environment variables
- Run configurations
- Optional dependency diagnostics

## UI

- Custom themes
- Animated backgrounds
- Application icons
- Multiple dashboard pages
- Compact/list view
- Grid-size controls
- Command palette
- Keyboard shortcuts
- Global hotkey

## Organisation

- Import/export launcher database
- Backup configuration
- Project grouping
- Application notes
- Automatic project detection
- Duplicate detection

---

# 🌌 Long-Term Vision

The launcher can eventually become a personal **JASS Software Center** for the applications developed over time.

```text
                    🚀 JASS FUTURE LAUNCHER
                              │
             ┌────────────────┼────────────────┐
             │                │                │
          🤖 AI             🎬 MEDIA        🌐 LANGUAGE
             │                │                │
        Athena tools      Subtitle tools    Mizo tools
        AI utilities      Video tools       Grammar tools
             │                │                │
             └────────────────┼────────────────┘
                              │
                         💻 OTHER TOOLS
                              │
                       Personal software
                           collection
```

The key principle remains:

> **The launcher organizes the applications; it does not own the applications.**

---

## ❤️ JASS Future Launcher

**One dashboard.  
All your applications.  
One click to launch.**
