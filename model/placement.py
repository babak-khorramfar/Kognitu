# model/placement.py


class Placement:
    """
    Represents one board tile placement.
    Attributes:
        x (float): X-coordinate in grid units (0 ≤ x < cols)
        y (float): Y-coordinate in grid units (0 ≤ y < rows)
        angle (int): rotation angle in degrees (0, 90, 180, 270)
        action (str): intended movement action (e.g., "walk", "jump", "turn")
        difficulty (str): difficulty level ("easy", "medium", "hard")
    """

    def __init__(
        self,
        x: float,
        y: float,
        angle: int = 0,
        action: str = "walk",
        difficulty: str = "easy",
    ):
        self.x = x
        self.y = y
        self.angle = angle % 360
        self.action = action
        self.difficulty = difficulty

    def to_dict(self) -> dict:
        """Convert to serializable dict."""
        return {
            "x": self.x,
            "y": self.y,
            "angle": self.angle,
            "action": self.action,
            "difficulty": self.difficulty,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Instantiate from dict."""
        return cls(
            x=data.get("x", 0),
            y=data.get("y", 0),
            angle=data.get("angle", 0),
            action=data.get("action", "walk"),
            difficulty=data.get("difficulty", "easy"),
        )
