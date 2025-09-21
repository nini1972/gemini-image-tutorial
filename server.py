import uvicorn
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from PIL import Image
from pathlib import Path

# Add the src directory to the Python path to allow for package imports
import sys
sys.path.append(str(Path(__file__).resolve().parent))

# Import your existing, well-structured image generation logic
from src.image_generator.core import generate_image

# --- API Data Models ---
# Define what the input to our API should look like
class ImageRequest(BaseModel):
    prompt: str
    base_image_paths: Optional[List[str]] = Field(default=None, description="List of local file paths for base images.")

# Define what the output from our API will look like
class ImageResponse(BaseModel):
    status: str
    message: str
    image_path: Optional[str] = None

# --- FastAPI Application ---
app = FastAPI(
    title="Gemini Image Generation Server (MCP)",
    description="An API to generate images using gemini-2.5-flash-image-preview. This server can be used as a tool by other applications, like CrewAI agents.",
    version="1.0.0"
)

@app.post("/generate-image/", response_model=ImageResponse)
async def create_image_endpoint(request: ImageRequest):
    """
    Generates an image based on a prompt and optional base images.
    Returns the path to the saved image.
    """
    print(f"Received request to generate image with prompt: {request.prompt}")
    
    pil_images = []
    if request.base_image_paths:
        for path_str in request.base_image_paths:
            path = Path(path_str)
            if not path.exists():
                raise HTTPException(status_code=400, detail=f"File not found: {path_str}")
            try:
                pil_images.append(Image.open(path))
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to open image {path_str}: {e}")

    try:
        # Call your core logic
        generated_image = generate_image(
            prompt=request.prompt,
            base_images=pil_images if pil_images else None
        )

        if generated_image:
            # Save the generated image to a file
            output_dir = Path("output")
            output_dir.mkdir(exist_ok=True)
            
            # Use timestamp-based naming to guarantee uniqueness
            timestamp = int(time.time() * 1000)  # milliseconds since epoch
            output_filename = f"server_generated_{Path.cwd().name}_{timestamp}.png"
            save_path = output_dir / output_filename
            
            generated_image.save(save_path)
            
            print(f"✅ Image successfully generated and saved to {save_path}")
            return {"status": "success", "message": "Image generated successfully.", "image_path": str(save_path)}
        else:
            # This handles cases where the model returns an empty response (e.g., safety filters)
            print("❌ Image generation failed. The model may have returned an empty response.")
            raise HTTPException(status_code=500, detail="Image generation failed. The model may have returned an empty response due to safety filters or other issues.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# --- Main entry point to run the server ---
if __name__ == "__main__":
    print("Starting Gemini Image Generation Server (MCP)...")
    print("Your CrewAI agents can now make requests to http://127.0.0.1:8000/generate-image/")
    print("Open your browser to http://127.0.0.1:8000/docs for interactive API documentation.")
    # Uvicorn is an ASGI server that runs our FastAPI application
    uvicorn.run(app, host="127.0.0.1", port=8000)
