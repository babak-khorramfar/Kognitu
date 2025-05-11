# model/tile.py


class Tile:
    """
    Represents a single board tile.
    Attributes:
        row (int): row index on the board
        col (int): column index on the board
        color (tuple[int,int,int]): RGB color
        rotation (int): rotation angle in degrees
    """

    def __init__(self, row: int, col: int, color: tuple[int, int, int]):
        self.row = row
        self.col = col
        self.color = color
        self.rotation = 0

    def rotate(self, angle: int):
        """Rotate tile by given angle (in degrees)."""
        self.rotation = (self.rotation + angle) % 360
