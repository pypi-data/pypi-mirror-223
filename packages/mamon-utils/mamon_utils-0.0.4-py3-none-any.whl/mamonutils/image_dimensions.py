import requests
from PIL import Image
from io import BytesIO
from typing import Dict


def get_dimensions(image_url: str) -> Dict[str, int]:
    # Validate if the provided image_url is a non-empty string
    if not isinstance(image_url, str) or not image_url.strip():
        raise ValueError("Invalid image. Please provide a valid URL string.")

    try:
        response = requests.get(image_url)
        # Raise an exception for 4xx and 5xx status codes.
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        width, height = img.size
        return {"width": width, "height": height}
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error fetching the image: {e}")
    except IOError as e:
        raise ValueError(f"Error processing the image: {e}")
