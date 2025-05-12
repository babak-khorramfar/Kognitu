# utils/config.py

"""
Central configuration for Kognitu project.
"""

# AI Model name
MODEL_NAME = "gpt2"

# Path to the tile image file (each tile should be a 60x60 PNG)
TILE_IMAGE_PATH = "resources/images/tile.png"

# Default grid rows/cols if needed
DEFAULT_ROWS = 3
DEFAULT_COLS = 3

# Factor for minimum spacing relative to tile size (to avoid overlap when rotated)
# e.g., 1.42 ensures no overlap at 45 degrees
DIAGONAL_SPACING_FACTOR = 1.42
