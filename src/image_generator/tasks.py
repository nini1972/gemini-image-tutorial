from PIL import Image
from io import BytesIO
from .core import client

def style_transfer(base_image_path, prompt):
    """
    Applies a style to a base image.

    Args:
        base_image_path (str): The path to the base image.
        prompt (str): The prompt describing the style to apply.

    Returns:
        PIL.Image.Image: The generated image.
    """
    base_object = Image.open(base_image_path)
    response = client.models.generate_content(
        model="gemini-2.5-flash-image-preview",
        contents=[
            prompt,
            base_object
        ]
    )
    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            return Image.open(BytesIO(part.inline_data.data))
    return None
