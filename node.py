import base64
import io
import logging
import requests
import numpy as np
from PIL import Image
from openai import OpenAI
from typing import List, Tuple, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Constants ---
ABACUS_BASE_URL = "https://routellm.abacus.ai/v1"
DEFAULT_MODEL = "route-llm"  # This mimics the "auto" behavior of the web chat
FALLBACK_MODELS = [DEFAULT_MODEL, "gpt-4o", "claude-3-5-sonnet", "gemini-1.5-pro"]
REQUEST_TIMEOUT = 5
MAX_TOKENS = 1024

def fetch_available_models() -> List[str]:
    """Fetches available models from Abacus API and ensures route-llm is prioritized.

    Returns:
        List of model IDs, with DEFAULT_MODEL first if available.
    """
    try:
        response = requests.get(f"{ABACUS_BASE_URL}/models", timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        models = [model["id"] for model in data.get("data", [])]

        # Prioritize DEFAULT_MODEL
        if DEFAULT_MODEL in models:
            models.remove(DEFAULT_MODEL)
        models.insert(0, DEFAULT_MODEL)

        if not models:
            logger.warning("No models returned from API, using fallbacks.")
            return FALLBACK_MODELS.copy()

        return models
    except Exception as e:
        logger.error(f"Failed to fetch models: {e}, using fallbacks.")
        return FALLBACK_MODELS.copy()

# Fetch models once at ComfyUI startup
AVAILABLE_MODELS = fetch_available_models()

def tensor_to_base64(image_tensor: np.ndarray) -> str:
    """Converts ComfyUI [B,H,W,C] tensor to base64 string.

    Args:
        image_tensor: Input image tensor.

    Returns:
        Base64 encoded string of the image.
    """
    # Take the first image in the batch
    image_array = (255. * image_tensor[0].cpu().numpy()).clip(0, 255).astype(np.uint8)
    img = Image.fromarray(image_array)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def call_openai_api(client: OpenAI, model: str, instructions: str, image_b64: str) -> Optional[str]:
    """Calls the OpenAI API to generate a prompt from image and instructions.

    Args:
        client: OpenAI client instance.
        model: Model to use.
        instructions: Text instructions.
        image_b64: Base64 encoded image.

    Returns:
        Generated text or None if error.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": instructions},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{image_b64}"}
                        },
                    ],
                }
            ],
            max_tokens=MAX_TOKENS,
        )
        return response.choices[0].message.content if response.choices else None
    except Exception as e:
        logger.error(f"API call failed: {e}")
        return None

class ImageToPromptAbacus:
    """ComfyUI node for generating image prompts using Abacus.AI API."""

    @classmethod
    def INPUT_TYPES(cls) -> dict:
        return {
            "required": {
                "image": ("IMAGE",),
                "instructions": ("STRING", {
                    "multiline": True,
                    "default": "Describe this image in detail for an image generation prompt."
                }),
                "model": (AVAILABLE_MODELS, {"default": AVAILABLE_MODELS[0]}),
                "api_key": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "convert"
    CATEGORY = "Abacus.AI"

    def convert(self, image: np.ndarray, instructions: str, model: str, api_key: str) -> Tuple[str]:
        """Converts image to prompt text using AI.

        Args:
            image: Input image tensor.
            instructions: Prompt instructions.
            model: AI model to use.
            api_key: API key for authentication.

        Returns:
            Tuple containing the generated text or error message.
        """
        if not api_key.strip():
            return ("Error: API Key is required.",)

        client = OpenAI(api_key=api_key, base_url=ABACUS_BASE_URL)
        image_b64 = tensor_to_base64(image)

        result = call_openai_api(client, model, instructions, image_b64)
        if result is None:
            return ("Error: Failed to generate prompt from API.",)

        return (result,)

NODE_CLASS_MAPPINGS = {
    "ImageToPromptAbacus": ImageToPromptAbacus
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageToPromptAbacus": "Image to Prompt (Abacus.AI)"
}