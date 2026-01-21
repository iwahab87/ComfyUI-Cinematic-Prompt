print("--- CINEMATIC NODE: INITIALIZING ---")

from .cinematic_node import CinematicPromptNode

NODE_CLASS_MAPPINGS = {
    "CinematicPromptNode": CinematicPromptNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CinematicPromptNode": "Cinematic Prompt Builder (Yedp)"
}

# This line tells ComfyUI where to find the JS file.
# It MUST point to the "web" folder inside your node folder.
WEB_DIRECTORY = "./web"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]