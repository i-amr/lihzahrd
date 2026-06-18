from dataclasses import dataclass


@dataclass
class Layers:
    """Stores the Y-level boundaries of each Terraria world layer."""
    surface: float
    underground: float
    hell: float  # world full height
    sky: float = 0.0
    cavern: float = 0.0

    def __post_init__(self):
        if not self.sky:
            self.sky = self.surface * 0.35
        if not self.cavern:
            self.cavern = self.hell - 200
