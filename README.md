# Gemini Image Tutorial (example)

This repo shows a small example using the `google-genai` library together with `python-dotenv` and `Pillow`.

Setup (using `uv`):

```powershell
# Install dependencies into a project-managed virtual environment
uv add google-genai python-dotenv pillow

# Activate the created venv (PowerShell)
.\.venv\Scripts\Activate.ps1
```

Run the import example:

```powershell
python examples\genai_basic.py
```

Notes
- The `google-genai` package exposes its API under the `google.genai` namespace. Use `from google.genai import ...`.
- The example avoids making network calls and only validates imports and basic client construction.
