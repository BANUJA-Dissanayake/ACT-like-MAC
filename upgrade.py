import os
import time

APPS_FILE = os.path.join(os.path.dirname(__file__), "apps.txt")

apps = []
with open(APPS_FILE, "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if line.endswith(","):
            line = line[:-1].strip()
        if line.startswith("r\"") or line.startswith("r'"):
            line = line[1:]
        if (line.startswith('"') and line.endswith('"')) or (line.startswith("'") and line.endswith("'")):
            line = line[1:-1]

        apps.append(line)

for app in apps:
    try:
        if os.path.exists(app):
            os.startfile(app)
            print(f"Opened: {app}")
        else:
            print(f"Skipping missing file: {app}")
        time.sleep(1)
    except Exception as e:
        print(f"Could not open {app}: {e}")

print("\nDone! All apps launched.")
input("Press Enter to close this window...")