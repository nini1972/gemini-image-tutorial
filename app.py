import sys
from pathlib import Path
import requests

# Add the src directory to the Python path to allow for package imports
sys.path.append(str(Path(__file__).resolve().parent))

from src.image_generator.core import generate_and_save_image
from src.image_generator.tasks import style_transfer

def main():
    """Main function to run image generation tasks."""
    print("--- Running Core Image Generation ---")
    generate_and_save_image(
        "A futuristic cityscape at sunset, with flying cars and neon signs.",
        "futuristic_city.png"
    )

    print("\n--- Running Style Transfer Task ---")
    
    # Define the base image path and URL
    base_image_filename = "chair.png"
    base_image_path = Path("images") / base_image_filename
    image_url = "https://cdn-images-1.medium.com/proxy/1*TWO2meqMNnS1-6XSO6yv7Q.png"

    # Create images directory if it doesn't exist
    base_image_path.parent.mkdir(exist_ok=True)

    # Download the image if it doesn't exist
    if not base_image_path.exists():
        print(f"Downloading base image to {base_image_path}...")
        try:
            response = requests.get(image_url)
            response.raise_for_status()  # Raise an exception for bad status codes
            with open(base_image_path, "wb") as f:
                f.write(response.content)
            print("✅ Base image downloaded.")
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to download base image: {e}")
            return

    # Perform style transfer
    style_prompt = "Change this chair into a whimsical, fairytale style with floral patterns and pastel colors."
    generated_image = style_transfer(str(base_image_path), style_prompt)

    if generated_image:
        output_filename = "styled_chair.png"
        output_path = Path("images") / output_filename
        generated_image.save(output_path)
        print(f"✅ Styled image saved as {output_path}")
    else:
        print("❌ Style transfer failed.")

if __name__ == "__main__":
    main()