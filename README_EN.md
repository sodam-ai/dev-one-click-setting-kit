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
5. [Key features](#key-features)
6. [Folder structure](#folder-structure)
7. [FAQ](#faq)
8. [Important notes](#important-notes)
9. [License](#license)

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
| Beginner | Windows Terminal | Better terminal experience |
| Intermediate | GitHub CLI | GitHub command-line operations |
| Intermediate | PowerShell 7 | Enhanced scripting environment |
| Intermediate | pnpm | Fast package manager |
| Intermediate | Ollama | Run local AI models |
| Intermediate | Bun | Ultra-fast JS runtime |
| Advanced | Java 21 LTS | Enterprise backend development |
| Advanced | Flutter + Dart | Mobile/desktop app development |
| Advanced | Go | High-performance server development |
| Advanced | Rust | Systems/security programming |
| New | Ruby | Web backend (Rails) |
| New | PHP | Web backend (Laravel) |

### Optional npm packages

Vercel · Supabase · Stripe CLI · Railway CLI · Prisma · Claude CLI · Uploadthing

---

## How to use — Complete beginner guide

### Requirements

- Windows 10 (21H2 or later) or Windows 11
- Internet connection
- `dev-one-click-setting-kit.bat` file

### Steps

#### Step 1 — Download the file

Click the green **`<> Code`** button at the top right of this page  
→ Click **`Download ZIP`**  
→ Extract the downloaded ZIP file

#### Step 2 — Run as Administrator

Right-click on `dev-one-click-setting-kit.bat`  
→ Select **"Run as administrator"**

> ⚠️ Without administrator rights, some tools may not install correctly.

#### Step 3 — Choose from the menu

A black terminal window will open with a menu.  
Type a number and press **Enter**.

```
============================================================
   Vibe Coder Environment Kit
============================================================

 [1] Beginner Install    ← Start here if you're new
 [2] Intermediate Install
 [3] Advanced Install
 [4] New Tools
 [5] Select Individual Tools
 [6] Update
 [7] Remove (individual)
 [8] Remove All
 [9] Check Installation
 [0] Exit
```

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

After installation, two files are automatically saved in the same folder:

| File | Contents |
|------|----------|
| `install-report-DATE.txt` | Success/fail/skip summary |
| `install-log-DATE.txt` | Detailed installation log |

---

## Installation levels

| Level | Who it's for | Total tools |
|-------|-------------|-------------|
| **[1] Beginner** | First-time vibe coders | 5 |
| **[2] Intermediate** | After completing Beginner level | 10 |
| **[3] Advanced** | Multi-language development | 14 |
| **[4] New** | Specialized languages (Ruby, PHP) | 16 |

> If you're just starting out, **[1] Beginner** level is all you need.

---

## Key features

| Feature | Description |
|---------|-------------|
| One-click install | Automatically installs tools via Windows' built-in winget |
| Already-installed detection | Choose to skip / upgrade / remove |
| Auto-retry | Automatically retries once on failure |
| Portable | Works regardless of BAT file location or filename |
| Install report | Saves results as a text file automatically |
| PATH verification | Checks environment variable registration after install |
| CLI cheat sheet | Shows version check commands after completion |
| Individual selection | Pick specific tools from a numbered list [1]–[26] |
| Update menu | Bulk update npm packages |
| Remove menu | Individual or full removal support |

---

## Folder structure

```
dev-one-click-setting-kit.bat   ← Main executable (this is all you need)
README.md                       ← Korean guide
README_EN.md                    ← English guide (this file)
LICENSE                         ← License
PRD/                            ← Development planning docs (reference only)
  01_PRD.md
  02_DATA_MODEL.md
  03_PHASES.md
  04_PROJECT_SPEC.md
```

> `install-report-*.txt` and `install-log-*.txt` are generated automatically after running.  
> These files are listed in `.gitignore` and will not be uploaded to GitHub.

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
- **Log files** — `install-log-*.txt` contains no sensitive data, but verify before sharing.
- **Safe to re-run** — Running again on a configured PC will not break existing installations.

---

## License

MIT License — Free to use, modify, and distribute.  
Copyright © 2026 **SoDam AI Studio**  
See [LICENSE](./LICENSE) for full terms.
