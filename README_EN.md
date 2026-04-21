# DEV-KIT — One-Click Vibe Coding Environment Setup Kit

> Automatically installs an AI vibe coding development environment on Windows PC **with a single click**.  
> No coding experience required.

**[한국어 가이드 →](./README.md)**

---

## Table of Contents

1. [What is this?](#what-is-this)
2. [What tools get installed?](#what-tools-get-installed)
3. [How to use — Complete beginner guide](#how-to-use--complete-beginner-guide)
4. [Installation levels](#installation-levels)
5. [Direct Download Menu](#direct-download-menu-8)
6. [Key features](#key-features)
7. [Folder structure](#folder-structure)
8. [FAQ](#faq)
9. [Important notes](#important-notes)
10. [License](#license)

---

## What is this?

"Vibe coding" means building software by talking to AI in natural language — no traditional programming required.  
Before you can start, your PC needs several development tools installed, which takes 30–60 minutes manually and is easy to get wrong.

**Just run `dev-one-click-setting-kit.bat` once** and it will:

- Automatically find and install all required tools
- Skip or upgrade tools that are already installed
- Save an installation report when done

> This file is **Windows only**. It does not work on macOS or Linux.

---

## What tools get installed?

### Core tools (via winget)

| Level | Tool | Purpose |
|-------|------|---------|
| Beginner | Git | Essential for saving and sharing code |
| Beginner | Python 3 | Core language for AI/ML development |
| Beginner | Node.js LTS | Required for web dev (Next.js, React, etc.) |
| Beginner | VS Code | Code editor |
| Beginner | Windows Terminal | Better terminal experience |
| Intermediate | GitHub CLI | GitHub command-line operations |
| Intermediate | PowerShell 7 | Enhanced scripting environment |
| Intermediate | pnpm | Fast package manager |
| Intermediate | Ollama | Run local AI models |
| Intermediate | Bun | Ultra-fast JS runtime |
| Advanced | Java 21 LTS | Enterprise backend development |
| Advanced | Flutter | Mobile/desktop app development |
| Advanced | Go | High-performance server development |
| Advanced | Rust | Systems/security programming |
| New | Ruby | Web backend (Rails) |
| New | PHP | Web backend (Laravel) |
| New | GitHub LFS | Large file storage |
| New | Stripe CLI | Payment development tool |

### Optional npm packages

Vercel · Supabase · Stripe CLI · Railway CLI · Prisma · Claude CLI · Uploadthing

> npm packages can be selected one by one with **Y/N** during installation.

---

## How to use — Complete beginner guide

### Requirements

- Windows 10 (21H2 or later) or Windows 11
- Internet connection
- `dev-one-click-setting-kit.bat` file

### Steps

#### Step 1 — Download the file

Click **[Releases](../../releases/latest)** on the top right of this page  
→ Under **Assets**, click `dev-one-click-setting-kit.bat` to save it

> Alternatively: click **`<> Code`** → **`Download ZIP`** → extract the ZIP file.

#### Step 2 — Run as Administrator

Right-click on `dev-one-click-setting-kit.bat`  
→ Select **"Run as administrator"**

> ⚠️ Without administrator rights, some tools may not install correctly.

#### Step 3 — Choose from the menu

A black terminal window will open with a menu.  
Type a number and press **Enter**.

```
===========================================================
   Vibe Coder Environment Kit | AI Dev Environment Setup
===========================================================

   [1] Beginner Install    First-timers        (5 tools,  ~7 min)
   [2] Intermediate         After Beginner      (11 tools, ~15 min)
   [3] Advanced             Multi-language dev  (16 tools, ~35 min)
   [4] New Tools            Extra tools         (18 tools, ~45 min)
   ---------------------------------------------------
   [5] Select Individual    Pick what you need
   [6] Update               Update all npm packages
   [7] Remove               Remove individual/all tools
   [8] Direct Download      Official site URLs  (if winget fails)
   [9] Check Installation   Show O/X + version info
   [0] Exit
```

> If you're new, type **`1`** and press Enter.

#### Step 4 — Handle already-installed tools

Before installation starts, if any tools are already installed, you'll be asked:

```
How to handle already-installed tools:
  [1] Skip      (keep current version)
  [2] Upgrade   (update to latest)
  [3] Remove    (uninstall only)
  Choice (default=1):
```

> Just press **Enter** to automatically select **[1] Skip**.

#### Step 5 — Check results

After installation, two files are automatically saved in the same folder, and total elapsed time is shown on screen.

| File | Contents |
|------|----------|
| `install-report-DATE.txt` | Success/fail/skip summary |
| `install-log-DATE.txt` | Detailed installation log |

---

## Installation levels

| Level | Who it's for | Total tools | Est. time |
|-------|-------------|-------------|-----------|
| **[1] Beginner** | First-time vibe coders | 5 | ~7 min |
| **[2] Intermediate** | After completing Beginner level | 11 | ~15 min |
| **[3] Advanced** | Multi-language development | 16 | ~35 min |
| **[4] New** | Specialized tools (Ruby, PHP, etc.) | 18 | ~45 min |

> If you're just starting out, **[1] Beginner** level is all you need.

---

## Direct Download Menu ([8])

When winget fails, select **[8]** from the main menu to see official download site URLs.  
Type a number or **Ctrl+click** a URL to open it in your browser instantly.

```
[Direct Download Links]
Type a number OR Ctrl+click a URL to open it in your browser.
---------------------------------------------------
  --- Beginner Tools ---     [1] Git  [2] Python  [3] Node.js  [4] VS Code  [5] Windows Terminal
  --- Intermediate ---       [6] GitHub CLI  [7] PowerShell 7  [8] pnpm  [9] Ollama  [10] Bun
  --- Advanced ---           [11] Java  [12] Flutter  [13] Go  [14] Rust
  --- New Tools ---          [15] Ruby  [16] PHP
  --- AI Tools ---           [17] Cursor  [18] Claude Desktop  [19] GitHub Desktop
  --- Dev CLI Extensions ---  [20] GitHub LFS  [21] Stripe CLI
```

> **Ctrl+click**: In the terminal, hold Ctrl and click the URL with your mouse to open the browser.

---

## Key features

| Feature | Description |
|---------|-------------|
| One-click install | Automatically installs tools via Windows' built-in winget |
| Already-installed detection | Choose to skip / upgrade / remove |
| Auto-retry | Automatically retries once on failure |
| Portable | Works regardless of BAT file location or filename |
| Install report | Saves results as a text file automatically |
| Elapsed time display | Shows total time taken after installation completes |
| PATH verification | Checks environment variable registration after install |
| CLI cheat sheet | Shows version check commands after completion |
| Individual selection | Pick specific tools from [1]–[18] |
| npm Y/N selection | Choose Vercel/Supabase/etc. one by one |
| Update menu | Bulk update npm packages |
| Direct Download menu | 21 official URLs — open with Ctrl+click |
| Remove menu | Individual or full removal support |
| Disk space check | Warns and pauses if less than 3 GB free |

---

## Folder structure

```
dev-one-click-setting-kit.bat   ← Main executable (this is all you need)
README.md                       ← Korean guide
README_EN.md                    ← English guide (this file)
CHANGELOG.md                    ← Version history
LICENSE                         ← License
PRD/                            ← Development planning docs (reference only)
upgrade_v1.1.0.py               ← v1.1.0 patch record script
```

> `install-report-*.txt` and `install-log-*.txt` are generated automatically after running.  
> `.bak` and log files are listed in `.gitignore` and will not be uploaded to GitHub.

---

## FAQ

**Q. Installation fails even with administrator rights?**

Windows Defender or antivirus software may be blocking the BAT file.  
Add the file to your antivirus whitelist, or temporarily disable real-time protection and try again.

---

**Q. The terminal window closed unexpectedly during installation?**

Open `install-log-DATE.txt` in the same folder and check the last few lines for error details.

---

**Q. "winget not found" error?**

Install **"App Installer"** from the Microsoft Store.  
Or go to Windows Settings → Apps → Optional Features → App Installer.

---

**Q. I only want to install specific tools?**

Choose **[5] Select Individual Tools** from the main menu to pick tools one by one.

---

**Q. A tool won't install via winget?**

Select **[8] Direct Download** from the main menu.  
Type a number or **Ctrl+click** a URL to open the official download page in your browser.

---

**Q. How do I update tools to the latest version?**

Use **[6] Update** from the main menu,  
or choose **[2] Upgrade** when prompted during a level install.

---

**Q. Is it safe to run again on a PC that's already set up?**

Yes. The default **Skip** mode means already-installed tools won't be touched.

---

## Important notes

- **Windows only** — Does not work on macOS or Linux.
- **Internet required** — winget downloads packages from the internet.
- **Corporate restrictions** — Some enterprise PCs may have winget blocked by IT policy.
- **Disk space** — Full installation requires about 5 GB free. A warning appears if less than 3 GB is available.
- **Log files** — `install-log-*.txt` contains no sensitive data, but verify before sharing.
- **Safe to re-run** — Running again on a configured PC will not break existing installations.

---

## License

MIT License — Free to use, modify, and distribute.  
Copyright © 2026 **SoDam AI Studio**  
See [LICENSE](./LICENSE) for full terms.
