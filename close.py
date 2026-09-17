import os
import subprocess
import sys

CLOSE_FILE = os.path.join(os.path.dirname(__file__), "apps.txt")


def clean_entry(line: str) -> str:
    line = line.strip()
    if line.endswith(","):
        line = line[:-1].strip()
    if line.startswith("r\"") or line.startswith("r'"):
        line = line[1:]
    if (line.startswith('"') and line.endswith('"')) or (line.startswith("'") and line.endswith("'")):
        line = line[1:-1]
    return line.strip()


def resolve_process_name(entry: str) -> str:
    path = clean_entry(entry)
    if path.lower().endswith(".lnk"):
        try:
            powershell = [
                "powershell",
                "-NoProfile",
                "-Command",
                f"$s=(New-Object -ComObject WScript.Shell).CreateShortcut('{path}'); Write-Output $s.TargetPath"
            ]
            result = subprocess.run(powershell, capture_output=True, text=True)
            if result.returncode == 0:
                target = result.stdout.strip()
                if target:
                    return os.path.basename(target)
        except Exception:
            pass

    if os.path.isabs(path):
        return os.path.basename(path)

    return path


def load_process_names(filepath):
    names = []
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            line = clean_entry(line)
            if line and not line.startswith("#"):
                names.append(resolve_process_name(line))
    return names


process_names = []
if os.path.exists(CLOSE_FILE):
    process_names = load_process_names(CLOSE_FILE)
else:
    fallback = os.path.join(os.path.dirname(__file__), "capps.txt")
    print(f"Warning: close list file not found: {CLOSE_FILE}")
    if os.path.exists(fallback):
        print(f"Using fallback list: {fallback}")
        process_names = load_process_names(fallback)

for name in process_names:
    try:
        result = subprocess.run(
            ["taskkill", "/F", "/IM", name],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"Closed: {name}")
        else:
            print(f"Not running or couldn't close: {name} ({result.stderr.strip()})")
    except Exception as e:
        print(f"Error closing {name}: {e}")

print("\nDone! Attempted to close all listed apps.")
if sys.stdin.isatty():
    input("Press Enter to close this window...")