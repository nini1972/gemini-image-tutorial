import os
from dotenv import load_dotenv
from google import genai
from PIL import Image
from io import BytesIO

# Load your API key from the .env file
load_dotenv()

# Create a client to talk to Gemini
client = genai.Client(api_key=os.getenv("GOOGLE_GENAI_API_KEY"))


def generate_and_save_image(prompt, filename):
   """
   Generate an image and save it to the images folder
  
   Args:
       prompt (str): Description of what you want to create
       filename (str): Name for the saved image file
  
   Returns:
       bool: True if successful, False otherwise
   """
   try:
       response = client.models.generate_content(
           model="gemini-2.5-flash-image-preview",
           contents=[prompt]
       )
      
       # Find and save the image
       for part in response.candidates[0].content.parts:
           if part.inline_data is not None:
               image = Image.open(BytesIO(part.inline_data.data))
               image.save(f"images/{filename}")
               print(f"✅ Image saved as images/{filename}")
               return True
              
   except Exception as e:
       print(f"❌ Error: {e}")
       return False
  
   return False
