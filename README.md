# Gemini Image Tutorial (example)

This repo shows a small example using the `google-genai` library together with `python-dotenv` and `Pillow`.

## Setup (using `uv`)

```powershell
# Install dependencies into a project-managed virtual environment
uv add google-genai python-dotenv pillow

# Activate the created venv (PowerShell)
.\.venv\Scripts\Activate.ps1
```

## Run the Application

The main entry point is `app.py`. It demonstrates how to use the `image_generator` package to perform tasks like basic image generation and style transfer.

```powershell
# Ensure your virtual environment is active
.\.venv\Scripts\Activate.ps1

# Run the main application
python app.py
```

The script will generate images and save them in the `output` directory.

## Project Structure

The project follows a standard `src` layout:

-   `app.py`: The main executable script.
-   `src/image_generator/`: A Python package containing the core logic.
    -   `core.py`: Handles the direct interaction with the Gemini API.
    -   `tasks.py`: Implements higher-level tasks (e.g., style transfer) using the core functions.
-   `.env`: Stores the `GOOGLE_GENAI_API_KEY`.
-   `output/`: The default directory where generated images are saved.

## How to activate the project's Python environment

Use the project-managed virtual environment (`.venv`) so your editor and runtime see the same installed packages.

### PowerShell (activate then run)

```powershell
# Activate the venv
.\.venv\Scripts\Activate.ps1

# Verify the active python executable
python -c "import sys; print(sys.executable)"

# Run the application
python app.py
```

If PowerShell blocks script execution, run:

```powershell
# Allow locally created scripts to run (choose only if you understand the security implications)
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### Run without activating (explicit interpreter)

```powershell
.\.venv\Scripts\python.exe app.py
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

### prompting guide and best practices

Describe the scene, don't just list keywords. The model's core strength is its deep language understanding. A narrative, descriptive paragraph will almost always produce a better, more coherent image than a list of disconnected words.

Best Practices
To elevate your results from good to great, incorporate these professional strategies into your workflow.

Be Hyper-Specific: The more detail you provide, the more control you have. Instead of "fantasy armor," describe it: "ornate elven plate armor, etched with silver leaf patterns, with a high collar and pauldrons shaped like falcon wings."
Provide Context and Intent: Explain the purpose of the image. The model's understanding of context will influence the final output. For example, "Create a logo for a high-end, minimalist skincare brand" will yield better results than just "Create a logo."
Iterate and Refine: Don't expect a perfect image on the first try. Use the conversational nature of the model to make small changes. Follow up with prompts like, "That's great, but can you make the lighting a bit warmer?" or "Keep everything the same, but change the character's expression to be more serious."
Use Step-by-Step Instructions: For complex scenes with many elements, break your prompt into steps. "First, create a background of a serene, misty forest at dawn. Then, in the foreground, add a moss-covered ancient stone altar. Finally, place a single, glowing sword on top of the altar."
Use "Semantic Negative Prompts": Instead of saying "no cars," describe the desired scene positively: "an empty, deserted street with no signs of traffic."
Control the Camera: Use photographic and cinematic language to control the composition. Terms like wide-angle shot, macro shot, low-angle perspective.

Limitations
For best performance, use the following languages: EN, es-MX, ja-JP, zh-CN, hi-IN.
Image generation does not support audio or video inputs.
The model won't always follow the exact number of image outputs that the user explicitly asked for.
The model works best with up to 3 images as an input.
When generating text for an image, Gemini works best if you first generate the text and then ask for an image with the text.
Uploading images of children is not currently supported in EEA, CH, and UK.
All generated images include a SynthID watermark.

Prompts for generating images
https://ai.google.dev/gemini-api/docs/image-generation#1_photorealistic_scenes
