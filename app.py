import sys
from pathlib import Path
import requests

# Add the src directory to the Python path to allow for package imports
sys.path.append(str(Path(__file__).resolve().parent))

from src.image_generator.core import generate_and_save_image
from src.image_generator.tasks import (
    style_transfer, 
    chat_with_image, 
    compose_images, 
    batch_generate_from_file,
    create_character_sheet
)

def main():
    """Main function to run image generation tasks."""
    
    print("Welcome to the Gemini Image Generation Tool!")
    print("What would you like to do?")
    print("1. Generate a new image from a prompt")
    print("2. Apply a style to an existing image")
    print("3. Start an interactive image refinement chat")
    print("4. Compose a new image from multiple images")
    print("5. Generate images in batch from a file")
    print("6. Create a consistent character and place them in scenes")
    
    choice = input("Enter your choice (1-6): ")

    if choice == '1':
        print("\n--- Running Core Image Generation ---")
        prompt = input("Enter the prompt for the image: ")
        filename = input("Enter the filename to save the image as (e.g., my_image.png): ")
        if prompt and filename:
            generate_and_save_image(prompt, filename)
        else:
            print("❌ Prompt and filename cannot be empty.")

    elif choice == '2':
        print("\n--- Running Style Transfer Task ---")
        
        base_image_path_str = input("Enter the path to the base image (e.g., images/chair.png): ")
        base_image_path = Path(base_image_path_str)

        if not base_image_path.exists():
            print(f"❌ Error: Base image not found at {base_image_path}")
            # Offer to download a sample
            download = input("Would you like to download a sample 'chair.png' image to the 'images' directory? (y/n): ")
            if download.lower() == 'y':
                base_image_filename = "chair.png"
                base_image_path = Path("images") / base_image_filename
                image_url = "https://cdn-images-1.medium.com/proxy/1*TWO2meqMNnS1-6XSO6yv7Q.png"
                base_image_path.parent.mkdir(exist_ok=True)
                try:
                    print(f"Downloading base image to {base_image_path}...")
                    response = requests.get(image_url)
                    response.raise_for_status()
                    with open(base_image_path, "wb") as f:
                        f.write(response.content)
                    print("✅ Base image downloaded.")
                except requests.exceptions.RequestException as e:
                    print(f"❌ Failed to download base image: {e}")
                    return
            else:
                return

        style_prompt = input("Enter the style prompt: ")
        if not style_prompt:
            print("❌ Style prompt cannot be empty.")
            return

        generated_image = style_transfer(str(base_image_path), style_prompt)

        if generated_image:
            output_filename = input("Enter the filename for the styled image (e.g., styled_chair.png): ")
            if not output_filename:
                output_filename = "styled_image.png"
            
            output_path = Path("output") / output_filename
            output_path.parent.mkdir(exist_ok=True)
            generated_image.save(output_path)
            print(f"✅ Styled image saved as {output_path}")
        else:
            print("❌ Style transfer failed.")

    elif choice == '3':
        print("\n--- Starting Image Refinement Chat ---")
        chat_with_image()

    elif choice == '4':
        print("\n--- Starting Multi-Image Composition ---")
        compose_images()

    elif choice == '5':
        print("\n--- Starting Batch Generation ---")
        batch_generate_from_file()

    elif choice == '6':
        print("\n--- Starting Character Creator ---")
        create_character_sheet()

    else:
        print("Invalid choice. Please run the script again and enter a number from 1 to 6.")


if __name__ == "__main__":
    main()