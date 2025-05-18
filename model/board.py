# model/board.py

from .tile import Tile
from typing import List, Tuple


class Board:
    """
    Represents the board, a grid of Tiles.
    Attributes:
        rows (int), cols (int)
        tiles (List[Tile])
    """

    def __init__(
        self, rows: int, cols: int, default_colors: List[Tuple[int, int, int]]
    ):
        self.rows = rows
        self.cols = cols
        self.default_colors = default_colors
        self.tiles: List[Tile] = []
        self.reset()

    def reset(self):
        """Initialize tiles in a simple pattern using default colors."""
        self.tiles.clear()
        for r in range(self.rows):
            for c in range(self.cols):
                idx = (r * self.cols + c) % len(self.default_colors)
                color = self.default_colors[idx]
                self.tiles.append(Tile(r, c, color))

    def get_tile_at(self, row: int, col: int) -> Tile | None:
        for tile in self.tiles:
            if tile.row == row and tile.col == col:
                return tile
        return None
