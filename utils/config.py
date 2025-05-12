# utils/config.py

"""
Central configuration for Kognitu project.
"""

# AI Model name (future use)
MODEL_NAME = "gpt2"

# Path to the tile image file (each tile should be a 60×60 PNG)
TILE_IMAGE_PATH = "resources/images/tile.png"

# Factor for spacing: sqrt(2) to avoid overlap when rotated
SPACING_FACTOR = 2**0.5
