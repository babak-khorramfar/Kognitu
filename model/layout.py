# model/layout.py

from dataclasses import dataclass
from typing import List


@dataclass
class Placement:
    x: int
    y: int
    angle: int = 0


class Layout:
    def __init__(self, placements: List[Placement]):
        self.placements = placements

    @staticmethod
    def auto_grid(count: int):
        # محاسبه تعداد ستون/ردیف برای مربعی‌شدن
        cols = int(count**0.5)
        if cols * cols < count:
            cols += 1
        rows = (count + cols - 1) // cols

        placements = []
        i = 0
        for r in range(rows):
            for c in range(cols):
                if i >= count:
                    break
                placements.append(Placement(c, r))
                i += 1
            if i >= count:
                break
        return Layout(placements)
