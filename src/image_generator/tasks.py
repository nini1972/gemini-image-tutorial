from PIL import Image
from pathlib import Path
from .core import generate_image

def style_transfer(base_image_path, prompt):
    """
    Applies a style to a base image using a prompt.

    Args:
        base_image_path (str): The path to the base image.
        prompt (str): The prompt describing the style to apply.

    Returns:
        PIL.Image.Image: The generated image object, or None.
    """
    try:
        base_object = Image.open(base_image_path)
        return generate_image(prompt, base_images=[base_object])
    except FileNotFoundError:
        print(f"❌ Error: Base image not found at {base_image_path}")
        return None
    except Exception as e:
        print(f"❌ Error during style transfer: {e}")
        return None

def chat_with_image():
    """
    Starts an interactive chat session to generate and refine an image.
    """
    print("🎨 Welcome to the Image Refinement Chat!")
    print("First, let's create an initial image.")
    
    try:
        # 1. Initial Generation
        initial_prompt = input("Enter the prompt for the first image: ")
        current_image = generate_image(initial_prompt)

        if not current_image:
            print("Could not generate the initial image. Exiting.")
            return

        print("✅ Initial image generated.")
        current_image.show(title="Initial Image")

        # 2. Refinement Loop
        while True:
            print("\nWhat would you like to do next?")
            refinement_prompt = input("Enter a refinement prompt (or type 'save', 'show', or 'quit'): ")

            if refinement_prompt.lower() in ['quit', 'exit']:
                print("Exiting chat. Your final image was not saved.")
                break
            
            if refinement_prompt.lower() == 'show':
                print("Displaying current image...")
                current_image.show(title="Current Image")
                continue

            if refinement_prompt.lower() == 'save':
                output_dir = Path("output")
                output_dir.mkdir(exist_ok=True)
                filename = input("Enter a filename for your image (e.g., my_creation.png): ")
                if not filename:
                    filename = "refined_image.png" # a default
                
                save_path = output_dir / filename
                try:
                    current_image.save(save_path)
                    print(f"✅ Image saved successfully to {save_path}")
                except Exception as e:
                    print(f"❌ Failed to save image: {e}")
                
                print("Exiting chat. Have a great day!")
                break

            # Refine the image
            print("🖌️  Refining image based on your prompt...")
            refined_image = generate_image(refinement_prompt, base_images=[current_image])

            if refined_image:
                current_image = refined_image
                print("✅ Refinement complete.")
                current_image.show(title="Refined Image")
            else:
                print("⚠️ Could not refine the image. The previous image is kept.")

    except (KeyboardInterrupt, EOFError):
        print("\n👋 Chat interrupted. Exiting.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def compose_images():
    """
    Starts an interactive session to compose a new image from multiple source images.
    """
    print("🖼️  Welcome to the Multi-Image Composition Tool!")
    print("Provide paths to local images you want to combine.")
    
    image_paths = []
    while True:
        path_input = input(f"Enter path for image {len(image_paths) + 1} (or press Enter to finish): ")
        if not path_input:
            if len(image_paths) < 2:
                print("❌ You need at least two images to compose. Please add more.")
                continue
            else:
                break
        
        image_path = Path(path_input.strip())
        if image_path.exists():
            image_paths.append(image_path)
            print(f"✅ Added '{image_path.name}'")
        else:
            print(f"❌ File not found at '{image_path}'. Please check the path and try again.")

    print("\n--- Images Loaded ---")
    for path in image_paths:
        print(f"- {path}")

    try:
        # Load PIL images
        pil_images = [Image.open(p) for p in image_paths]

        # Get composition prompt
        print("\nNow, describe how to combine these images.")
        prompt = input("Composition prompt (e.g., 'Place the person from the first image into the city background'): ")

        if not prompt:
            print("❌ Composition prompt cannot be empty. Exiting.")
            return

        # Generate the composed image
        print("🎨 Composing image based on your prompt...")
        composed_image = generate_image(prompt, base_images=pil_images)

        if composed_image:
            print("✅ Composition complete!")
            composed_image.show(title="Composed Image")
            
            # Save the result
            save = input("Would you like to save this image? (y/n): ")
            if save.lower() == 'y':
                output_dir = Path("output")
                output_dir.mkdir(exist_ok=True)
                filename = input("Enter a filename (e.g., composition.png): ")
                if not filename:
                    filename = "composed_image.png"
                
                save_path = output_dir / filename
                composed_image.save(save_path)
                print(f"✅ Image saved to {save_path}")
        else:
            print("❌ Failed to compose the image.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def batch_generate_from_file():
    """
    Generates images in a batch from a text file containing prompts.
    """
    print("📚 Welcome to the Batch Image Generation Tool!")
    print("Create a text file (e.g., prompts.txt) with one image prompt per line.")
    
    prompts_file_path_str = input("Enter the path to your prompts file: ")
    prompts_file_path = Path(prompts_file_path_str.strip())

    if not prompts_file_path.exists():
        print(f"❌ Error: File not found at '{prompts_file_path}'.")
        return

    try:
        with open(prompts_file_path, 'r') as f:
            prompts = [line.strip() for line in f if line.strip()]

        if not prompts:
            print("❌ No valid prompts found in the file.")
            return

        print(f"Found {len(prompts)} prompts. Starting batch generation...")
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        for i, prompt in enumerate(prompts):
            print(f"🔄 Generating image {i + 1}/{len(prompts)} for prompt: '{prompt}'")
            image = generate_image(prompt)
            if image:
                filename = f"batch_{i + 1:03d}.png"
                save_path = output_dir / filename
                image.save(save_path)
                print(f"✅ Saved as {save_path}")
            else:
                print(f"❌ Failed to generate image for prompt: '{prompt}'")
        
        print("\n🎉 Batch generation complete!")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def create_character_sheet():
    """
    Guides the user to create a character and then generate images of that character
    in different scenarios. Now supports starting from an existing image.
    """
    print("👤 Welcome to the Character Consistency Tool!")
    
    character_image = None
    
    try:
        # --- Ask user to create or load character ---
        choice = input("Do you want to (1) create a new character or (2) use an existing image file? Enter 1 or 2: ")

        if choice == '1':
            # 1a. Create the character reference sheet
            character_prompt = input("Describe your character in detail (e.g., 'A stoic female knight with a silver ponytail, wearing dark grey steel armor'): ")
            if not character_prompt:
                print("❌ Character description cannot be empty.")
                return

            print("👤 Generating character reference image...")
            character_image = generate_image(character_prompt)

            if not character_image:
                print("❌ Could not create the character reference. Aborting.")
                return

            print("✅ Character reference created!")
            character_image.show(title="Character Reference")

            # 1b. Immediately save the new character
            save = input("Would you like to save this character reference image? (y/n): ")
            if save.lower() == 'y':
                output_dir = Path("output")
                output_dir.mkdir(exist_ok=True)
                filename = input("Enter filename for character (e.g., my_character.png): ")
                if not filename:
                    filename = "character_reference.png"
                save_path = output_dir / filename
                character_image.save(save_path)
                print(f"✅ Character saved to {save_path}")

        elif choice == '2':
            # 2. Load existing character
            path_input = input("Enter the path to your character image file: ")
            image_path = Path(path_input.strip())
            if image_path.exists():
                character_image = Image.open(image_path)
                print(f"✅ Loaded character '{image_path.name}'")
                character_image.show(title=f"Loaded Character: {image_path.name}")
            else:
                print(f"❌ File not found at '{image_path}'. Aborting.")
                return
        else:
            print("Invalid choice. Exiting.")
            return

        # --- Scene Generation Loop ---
        if not character_image:
            print("No character image available to proceed. Exiting.")
            return

        while True:
            print("\nNow, let's place this character in a new scene.")
            scene_prompt = input("Describe the scene (or type 'quit'): ")

            if scene_prompt.lower() in ['quit', 'exit']:
                break

            full_prompt = f"Place the character from the reference image in this scene: {scene_prompt}"
            
            print("🎬 Generating new scene...")
            scene_image = generate_image(full_prompt, base_images=[character_image])

            if scene_image:
                print("✅ Scene generated!")
                scene_image.show(title="New Scene")
                save = input("Save this scene? (y/n): ")
                if save.lower() == 'y':
                    output_dir = Path("output")
                    output_dir.mkdir(exist_ok=True)
                    filename = input("Enter filename (e.g., character_scene.png): ")
                    if not filename:
                        filename = "character_scene.png"
                    save_path = output_dir / filename
                    scene_image.save(save_path)
                    print(f"✅ Saved to {save_path}")
            else:
                print("❌ Failed to generate the new scene.")

    except (KeyboardInterrupt, EOFError):
        print("\n👋 Exiting Character Creator.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

