# Cricbuzz Live Score with Playwright

Capture a live cricket score from Cricbuzz and save a screenshot as `score.png`.
The script waits for Cricbuzz's live-score status element rather than sleeping
for a fixed duration. If no live match appears, it reports that and still saves
a screenshot of the page.

## Setup (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
```

If PowerShell blocks activation, allow scripts for the current terminal only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Run

Run headed first to watch Chromium open:

```powershell
python cricbuzz_score.py
```

Run headless:

```powershell
python cricbuzz_score.py --headless
```
