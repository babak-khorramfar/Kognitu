# utils/config.py

"""
Central configuration for Kognitu project.
"""

# AI Model
MODEL_NAME = (
    "gpt2"  # later swap to a stronger model like "mistralai/Mistral-7B-Instruct"
)

# Board defaults
DEFAULT_ROWS = 2
DEFAULT_COLS = 2

# Core colors (در صورت نیاز برای حالت رنگ‌بندی)
DEFAULT_COLORS = [
    (255, 0, 0),  # Red
    (0, 255, 0),  # Green
    (0, 0, 255),  # Blue
    (255, 255, 0),  # Yellow
]

# Path to the tile image file (each tile should be a 60×60 PNG)
TILE_IMAGE_PATH = "resources/images/tile.png"

# Prompt template for AI layout generation
PROMPT_TEMPLATE = (
    "Generate a JSON with 'rows', 'cols', and 'placements' for a {rows}x{cols} board. "
    "Each placement must include x, y, angle (0|90|180|270), action (walk/jump/turn), "
    "and difficulty (easy/medium/hard). Example: "
    '{"rows":2,"cols":2,"placements":[{"x":0,"y":0,"angle":0,"action":"walk","difficulty":"easy"},...]}'
)
