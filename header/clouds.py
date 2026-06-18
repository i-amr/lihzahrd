class Clouds:
    """Information about... the clouds in the world?"""

    def __init__(self, is_active: int, cloud_number: int, wind_speed: float):
        self.is_active: int = is_active
        self.cloud_number: int = cloud_number
        self.wind_speed: float = wind_speed

    def __repr__(self):
        return f"WorldClouds(is_active={self.is_active}, cloud_number={self.cloud_number}, wind_speed={self.wind_speed})"
