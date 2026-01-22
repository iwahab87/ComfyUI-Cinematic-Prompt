print("--- CINEMATIC SUITE: INITIALIZING ---")

from .cinematic_node import CinematicPromptNode, CinematicLoaderNode

NODE_CLASS_MAPPINGS = {
    "CinematicPromptNode": CinematicPromptNode,
    "CinematicLoaderNode": CinematicLoaderNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CinematicPromptNode": "Cinematic Prompt Builder (Yedp)",
    "CinematicLoaderNode": "Cinematic Reference Loader (Yedp)"
}

WEB_DIRECTORY = "./web"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
