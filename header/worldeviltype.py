import enum


class WorldEvilType(enum.IntEnum):
    CORRUPTION = 0
    CRIMSON = 1

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"

    def __str__(self):
        return self.name.capitalize()
