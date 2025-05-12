# utils/config.py

"""
Central configuration for Kognitu project.
"""

# AI Model name
MODEL_NAME = "gpt2"

# Path to the tile image file (each tile should be a 60x60 PNG)
TILE_IMAGE_PATH = "resources/images/tile.png"

# Factor for minimum spacing relative to tile size (to avoid overlap when rotated)
# sqrt(2)-1 ≈ 0.41421356
DIAGONAL_SPACING_FACTOR = 0.41421356
