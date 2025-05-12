# model/layout.py

import json
import math
from typing import List
from .placement import Placement


class Layout:
    """
    Represents a full board layout:
      - rows, cols: dimensions
      - placements: list of Placement instances
    """

    def __init__(self, rows: int, cols: int, placements: List[Placement] = None):
        self.rows = rows
        self.cols = cols
        self.placements = placements[:] if placements else []

    @classmethod
    def auto_grid(cls, count: int):
        """
        Automatically create a nearly square grid layout for `count` items.
        Items are placed in row-major order.
        """
        cols = int(math.sqrt(count))
        if cols < 1:
            cols = 1
        rows = math.ceil(count / cols)
        placements = []
        for i in range(count):
            r = i // cols
            c = i % cols
            placements.append(Placement(x=c, y=r))
        return cls(rows, cols, placements)

    def add(self, placement: Placement):
        """Add a new placement."""
        self.placements.append(placement)

    def clear(self):
        """Remove all placements."""
        self.placements.clear()

    def to_dict(self) -> dict:
        """Convert entire layout to serializable dict."""
        return {
            "rows": self.rows,
            "cols": self.cols,
            "placements": [p.to_dict() for p in self.placements],
        }

    def to_json(self) -> str:
        """JSON string of layout."""
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: dict):
        """Instantiate Layout from dict."""
        rows = data.get("rows", 0)
        cols = data.get("cols", 0)
        placements_data = data.get("placements", [])
        placements = [Placement.from_dict(p) for p in placements_data]
        return cls(rows, cols, placements)

    @classmethod
    def from_json(cls, s: str):
        """Instantiate Layout from JSON string."""
        data = json.loads(s)
        return cls.from_dict(data)
