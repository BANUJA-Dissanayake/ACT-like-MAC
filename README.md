# ACT-like-MAC
This project is a lightweight utility designed to bring a smooth, macOS-like application launch experience to Windows. It automatically opens and launches all your essential Windows applications at once, streamlining your startup workflow and saving you time every time you boot up your computer.

Here is a complete, clean, and professional layout ready to paste directly into your GitHub `README.md` file.

---

# Windows Auto App Controller

An automated Python tool that brings a macOS-like app management experience to Windows. It allows you to launch or close all your configured desktop applications, shortcuts, and utilities simultaneously with a single click.

## Description

This project automates application management on Windows systems. Instead of searching through the Start Menu or clicking multiple desktop icons every time you turn on your computer, this script reads target paths from a central configuration file (`apps.txt`) and executes them sequentially. It also provides a dedicated utility to force-close all listed background processes when you want to clean up your workspace.

## How It Works

The project works through three core components:

* **Central Configuration (`apps.txt`):** Stores a list of raw file paths, Windows Start Menu shortcuts (`.lnk`), and system commands. This acts as the single source of truth for both opening and closing operations.


* **Automated Launcher (`upgrade.py`):** Reads `apps.txt` line-by-line, cleans up path formatting, and verifies that each target shortcut exists on your system. It then uses Python's `os.startfile()` function to launch each application cleanly with a 1-second pause between each app to prevent CPU spikes during startup.


* **Smart App Terminator (`close.py`):** Parses the shortcut paths listed in `apps.txt` and uses PowerShell commands to resolve `.lnk` shortcut files down to their actual executable process names (such as `chrome.exe` or `Discord.exe`). It then runs Windows `taskkill` commands to automatically terminate all running target applications at once.



## Code Explanation

* **Formatting & Path Cleaning:** The scripts automatically strip raw-string prefixes (`r""`), trailing commas, and quotes from `apps.txt` so paths can be processed by Windows without manual formatting errors.


* **Shortcut Resolution (`resolve_process_name`):** Windows shortcuts (`.lnk` files) don't match active process names directly. The program uses a PowerShell `WScript.Shell` COM object to inspect each shortcut and extract its real target executable.


* **Safe Execution:** The launcher utilizes native Windows file-handling (`os.startfile`) instead of aggressive command-line subprocesses, ensuring apps open with their default user permissions and working directories.
