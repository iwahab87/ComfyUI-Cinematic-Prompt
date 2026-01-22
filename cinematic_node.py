import nodes
import os
import torch
import numpy as np
from PIL import Image

class CinematicPromptNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt_state": ("STRING", {"default": "", "multiline": True, "hidden": True}),
                "positive_out": ("STRING", {"default": "", "multiline": True, "forceInput": False}),
                "negative_out": ("STRING", {"default": "", "multiline": True, "forceInput": False}),
            },
            "optional": {
                "clip": ("CLIP",), 
            }
        }

    RETURN_TYPES = ("CONDITIONING", "CONDITIONING", "STRING", "STRING")
    RETURN_NAMES = ("positive", "negative", "positive_text", "negative_text")
    FUNCTION = "process"
    CATEGORY = "Yedp/Prompting"

    def process(self, prompt_state, positive_out, negative_out, clip=None):
        cond_pos = []
        cond_neg = []

        if clip:
            try:
                tokens_pos = clip.tokenize(positive_out)
                cond, pooled = clip.encode_from_tokens(tokens_pos, return_pooled=True)
                cond_pos = [[cond, {"pooled_output": pooled}]]
                
                tokens_neg = clip.tokenize(negative_out)
                cond_n, pooled_n = clip.encode_from_tokens(tokens_neg, return_pooled=True)
                cond_neg = [[cond_n, {"pooled_output": pooled_n}]]
            except Exception as e:
                print(f"[Cinematic Prompt Error] Failed to encode: {e}")
        
        return (cond_pos, cond_neg, positive_out, negative_out)

class CinematicLoaderNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                # This input receives the filename (e.g., "camera_arri") from the JS
                "image_name": ("STRING", {"default": "", "multiline": False, "hidden": True}),
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "load_reference"
    CATEGORY = "Yedp/Prompting"

    def load_reference(self, image_name):
        # 1. Determine path to assets folder relative to this python file
        current_dir = os.path.dirname(os.path.realpath(__file__))
        assets_dir = os.path.join(current_dir, "web", "assets")
        
        # 2. Construct file path
        # Note: image_name comes from JS without extension to allow flexibility, or we handle it here
        # Let's assume JS sends "camera_arri" and we check extensions
        
        image_path = os.path.join(assets_dir, image_name)
        
        # Simple extension check
        if not os.path.exists(image_path):
            if os.path.exists(image_path + ".jpg"):
                image_path += ".jpg"
            elif os.path.exists(image_path + ".png"):
                image_path += ".png"
            else:
                # Fallback to a placeholder black image if file not found
                print(f"[Cinematic Loader] Error: Could not find image {image_name} in {assets_dir}")
                empty_img = torch.zeros(1, 512, 512, 3)
                empty_mask = torch.zeros(1, 512, 512)
                return (empty_img, empty_mask)

        # 3. Load and Convert Image (Standard ComfyUI loading logic)
        img = Image.open(image_path)
        
        # Handle Output 1: IMAGE (RGB Tensor)
        image = img.convert("RGB")
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,] # Add batch dimension [1, H, W, C]
        
        # Handle Output 2: MASK (Alpha channel if exists, else zero)
        if 'A' in img.getbands():
            mask = np.array(img.getchannel('A')).astype(np.float32) / 255.0
            mask = 1. - torch.from_numpy(mask)
        else:
            mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")
            
        return (image, mask)
