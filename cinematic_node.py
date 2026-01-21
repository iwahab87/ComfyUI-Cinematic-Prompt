import nodes

class CinematicPromptNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                # These are the text widgets manipulated by the JS
                "prompt_state": ("STRING", {"default": "", "multiline": True, "hidden": True}),
                "positive_out": ("STRING", {"default": "", "multiline": True, "forceInput": False}),
                "negative_out": ("STRING", {"default": "", "multiline": True, "forceInput": False}),
            },
            "optional": {
                # CLIP is optional so the node doesn't break if you just want text output
                "clip": ("CLIP",), 
            }
        }

    RETURN_TYPES = ("CONDITIONING", "CONDITIONING", "STRING", "STRING")
    RETURN_NAMES = ("positive", "negative", "positive_text", "negative_text")
    FUNCTION = "process"
    CATEGORY = "Yedp/Prompting"

    def process(self, prompt_state, positive_out, negative_out, clip=None):
        # Initialize empty results
        cond_pos = []
        cond_neg = []

        # Only process conditioning if a CLIP model is actually connected
        if clip:
            # 1. Encode Positive
            tokens_pos = clip.tokenize(positive_out)
            cond, pooled = clip.encode_from_tokens(tokens_pos, return_pooled=True)
            # CRITICAL FIX: Wrap in list + dict structure for ComfyUI
            cond_pos = [[cond, {"pooled_output": pooled}]]
            
            # 2. Encode Negative
            tokens_neg = clip.tokenize(negative_out)
            cond_n, pooled_n = clip.encode_from_tokens(tokens_neg, return_pooled=True)
            # CRITICAL FIX: Wrap in list + dict structure for ComfyUI
            cond_neg = [[cond_n, {"pooled_output": pooled_n}]]
        
        return (cond_pos, cond_neg, positive_out, negative_out)