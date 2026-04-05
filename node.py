import base64
import io
import requests
import numpy as np
from PIL import Image
from openai import OpenAI

# --- Fetch models at load time ---
ABACUS_BASE_URL = "https://routellm.abacus.ai/v1"
FALLBACK_MODELS = ["gpt-4o", "gpt-4-vision-preview", "claude-3-opus"]

def fetch_available_models():
    try:
        response = requests.get(f"{ABACUS_BASE_URL}/models", timeout=5)
        response.raise_for_status()
        data = response.json()
        models = [m["id"] for m in data.get("data", [])]
        return models if models else FALLBACK_MODELS
    except Exception as e:
        print(f"[AbacusAI] Failed to fetch models, using fallback list: {e}")
        return FALLBACK_MODELS

AVAILABLE_MODELS = fetch_available_models()


# --- Helper: Convert ComfyUI image tensor to base64 ---
def tensor_to_base64(image_tensor):
    # ComfyUI images are [B, H, W, C] float32 tensors in range [0, 1]
    # Handle both PyTorch tensors and numpy arrays
    if hasattr(image_tensor[0], 'numpy'):
        # PyTorch tensor
        image_np = (image_tensor[0].numpy() * 255).astype(np.uint8)
    else:
        # NumPy array
        image_np = (image_tensor[0] * 255).astype(np.uint8)
    pil_image = Image.fromarray(image_np)
    buffer = io.BytesIO()
    pil_image.save(buffer, format="PNG")
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("utf-8")


# --- The Node ---
class ImageToPromptAbacus:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "instructions": ("STRING", {
                    "multiline": True,
                    "default": "Describe this image as a detailed Stable Diffusion prompt."
                }),
                "model": (AVAILABLE_MODELS, {
                    "default": AVAILABLE_MODELS[0]
                }),
                "api_key": ("STRING", {
                    "multiline": False,
                    "default": ""
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "convert"
    CATEGORY = "Abacus.AI"
    OUTPUT_NODE = False

    def convert(self, image, instructions, model, api_key):
        # Convert image tensor to base64
        image_b64 = tensor_to_base64(image)

        # Init OpenAI-compatible client
        client = OpenAI(
            api_key=api_key,
            base_url=ABACUS_BASE_URL
        )

        # Build the message with image + instructions
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_b64}"
                            }
                        },
                        {
                            "type": "text",
                            "text": instructions
                        }
                    ]
                }
            ],
            max_tokens=1024
        )

        result = response.choices[0].message.content
        return (result,)


# --- Node Registration ---
NODE_CLASS_MAPPINGS = {
    "ImageToPromptAbacus": ImageToPromptAbacus
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageToPromptAbacus": "Image to Prompt (Abacus.AI)"
}