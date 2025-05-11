# utils/config.py

"""
Central configuration for Kognitu project.
"""

# AI Model
MODEL_NAME = "gpt2"  # later replace with e.g. "mistralai/Mistral-7B-Instruct"

# Board defaults
DEFAULT_ROWS = 2
DEFAULT_COLS = 2

# Core colors for tiles (RGB)
DEFAULT_COLORS = [
    (255, 0, 0),  # Red
    (0, 255, 0),  # Green
    (0, 0, 255),  # Blue
    (255, 255, 0),  # Yellow
]

# Prompt template
PROMPT_TEMPLATE = (
    "Generate a Python list of RGB tuples for a {rows}x{cols} board "
    "in row-major order. Example output: [(255,0,0),(0,255,0),...]."
)
