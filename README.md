# Gemini Image Tutorial (example)

This repo shows a small example using the `google-genai` library together with `python-dotenv` and `Pillow`.

## Setup (using `uv`)

```powershell
# Install dependencies into a project-managed virtual environment
uv add google-genai python-dotenv pillow

# Activate the created venv (PowerShell)
.\.venv\Scripts\Activate.ps1
```

## Run the import example

```powershell
python examples\genai_basic.py
```

## Notes
- The `google-genai` package exposes its API under the `google.genai` namespace. Use `from google.genai import ...`.
- The example avoids making network calls and only validates imports and basic client construction.

## How to activate the project's Python environment

Use the project-managed virtual environment (`.venv`) so your editor and runtime see the same installed packages.

### PowerShell (activate then run)

```powershell
# Activate the venv
.\.venv\Scripts\Activate.ps1

# Verify the active python executable
python -c "import sys; print(sys.executable)"

# Run the example
python examples\genai_basic.py
```

If PowerShell blocks script execution, run:

```powershell
# Allow locally created scripts to run (choose only if you understand the security implications)
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### Run without activating (explicit interpreter)

```powershell
.\.venv\Scripts\python.exe test_setup.py
```

### VS Code

- Open the Command Palette (Ctrl+Shift+P) → "Python: Select Interpreter" → choose the interpreter at
  `<repo-root>\.venv\Scripts\python.exe`.
- After switching the interpreter, reload the window (Developer: Reload Window) or restart the Python language server so Pylance picks up packages from the venv.

## Quick checks

- Confirm `dotenv` is available to the active interpreter:

```powershell
python -c "import dotenv; print(dotenv.__file__)"
```

- If `pip` is missing inside the venv, install it and upgrade:

```powershell
.\.venv\Scripts\python.exe -m ensurepip --upgrade
.\.venv\Scripts\python.exe -m pip install --upgrade pip
```

These steps ensure the editor and the runtime use the same environment so imports like `from dotenv import load_dotenv` resolve correctly.
