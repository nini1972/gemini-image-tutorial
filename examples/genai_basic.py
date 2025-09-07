"""Minimal example showing how to import and use google.genai.
This script does not perform any network calls; it demonstrates correct imports and
how to instantiate a client object (without credentials) for local testing.
"""

from google.genai import client
from dotenv import load_dotenv
import os


def main():
    print('google.genai client module:', client)

    # Load credentials from .env (do not commit real secrets)
    load_dotenv()
    api_key = os.getenv('GOOGLE_GENAI_API_KEY')
    project = os.getenv('GOOGLE_CLOUD_PROJECT')
    location = os.getenv('GOOGLE_CLOUD_LOCATION')

    # Try API-key-based instantiation first
    try:
        ClientClass = getattr(client, 'GenAIClient', None) or getattr(client, 'Client', None)
        if ClientClass is None:
            print('No Client class found in google.genai; this example only validates imports.')
            return

        if api_key:
            print('Attempting to instantiate client with API key from .env')
            try:
                c = ClientClass(api_key=api_key)
                print('Instantiated client with api_key:', type(c))
                return
            except Exception as e:
                print('Failed to instantiate with api_key (may require different arg names):', e)

        # Try Google Cloud / Vertex AI style (project & location)
        if project and location:
            print('Attempting to instantiate client with Google Cloud project/location from .env')
            try:
                c = ClientClass(vertexai=True, project=project, location=location)
                print('Instantiated client with Google Cloud args:', type(c))
                return
            except Exception as e:
                print('Failed to instantiate with Google Cloud args (expected if not configured):', e)

        print('No valid credentials found in .env or instantiation failed; example ends here.')

    except Exception as e:
        print('Client instantiation skipped/failed (expected without proper credentials):', e)


if __name__ == '__main__':
    main()
