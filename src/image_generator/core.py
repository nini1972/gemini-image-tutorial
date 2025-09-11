import os
from dotenv import load_dotenv
from google import genai
from PIL import Image
from io import BytesIO
from pathlib import Path

# Load your API key from the .env file
load_dotenv()

# Create a client to talk to Gemini
client = genai.Client(api_key=os.getenv("GOOGLE_GENAI_API_KEY"))


def generate_image(prompt, base_images=None):
    """
    Generates an image from a prompt, optionally using one or more base images.

    Args:
        prompt (str): The text prompt.
        base_images (list[PIL.Image.Image], optional): A list of base images for refinement or composition. Defaults to None.

    Returns:
        PIL.Image.Image: The generated image object, or None.
    """
    try:
        contents = [prompt]
        if base_images:
            contents.extend(base_images)

        response = client.models.generate_content(
            model="gemini-2.5-flash-image-preview",
            contents=contents
        )

        # --- Start of robust response handling ---
        if not response.candidates:
            print("❌ The model did not return any candidates. This might be due to a safety block.")
            # Try to print more details if available
            try:
                print(f"Prompt Feedback: {response.prompt_feedback}")
            except Exception:
                pass # Ignore if prompt_feedback is not available
            return None

        candidate = response.candidates[0]
        if not candidate.content or not candidate.content.parts:
            print("❌ The model's response was empty. This can happen if the prompt is blocked for safety reasons.")
            print(f"Finish Reason: {candidate.finish_reason}")
            print(f"Safety Ratings: {candidate.safety_ratings}")
            return None
        # --- End of robust response handling ---

        for part in candidate.content.parts:
            if part.inline_data is not None:
                return Image.open(BytesIO(part.inline_data.data))

    except Exception as e:
        print(f"❌ Error during image generation: {e}")
    
    return None


def generate_and_save_image(prompt, filename):
   """
   Generate an image and save it to the output folder
  
   Args:
       prompt (str): Description of what you want to create
       filename (str): Name for the saved image file
  
   Returns:
       bool: True if successful, False otherwise
   """
   image = generate_image(prompt)
   if image:
       try:
           # Ensure output directory exists
           output_dir = Path("output")
           output_dir.mkdir(exist_ok=True)
           
           image_path = output_dir / filename
           image.save(image_path)
           print(f"✅ Image saved as {image_path}")
           return True
       except Exception as e:
           print(f"❌ Error saving image: {e}")
   return False
