from __future__ import annotations

import math
from .powerid import PowerId
from ..fileutils import FileReader
from ..utility import Utils, Math


class Powers:
    """
    Manages Journey Mode power settings for a world or player.

    These settings control environment variables like time, weather, and
    difficulty scaling. Note that while most are stored in the world file,
    certain values like spawn rate are often handled per-session.
    """

    def __init__(
        self,
        time_locked  : bool  = False,
        set_dawn     : None  = None,
        set_noon     : None  = None,
        set_dusk     : None  = None,
        set_moon     : None  = None,
        time_rate    : float = 0.0,
        wind_strength: float = 0.0,    # Note: wld-header - these data are stored in the world file (.wld) header
        wind_locked  : bool  = False,
        rain_strength: float = 0.0,    # Note: wld-header - these data are stored in the world file (.wld) header
        rain_locked  : bool  = False,
        godmode      : bool  = False,  # Note: per-player - these data are stored in the player file (.plr)
        extend_range : bool  = False,  # Note: per-player - these data are stored in the player file (.plr)
        spawn_rate   : float = 0.5,    # Note: per-player - these data are stored in the player file (.plr)
        biome_spread : bool  = True,
        difficulty   : float = 0.33,
    ):
        # Time Management
        self._time_locked   = time_locked    # Toggle: Freeze time progression
        self._set_dawn      = set_dawn       # Button: Set time to 04:30 AM
        self._set_noon      = set_noon       # Button: Set time to 12:00 PM
        self._set_dusk      = set_dusk       # Button: Set time to 07:30 PM
        self._set_moon      = set_moon       # Button: Set time to 12:00 AM
        self._time_rate     = time_rate      # Slider: Time rate speed x1 to x24

        # Weather Control
        self._wind_strength = wind_strength  # Slider: Wind direction and velocity 40W to 40E
        self._wind_locked   = wind_locked    # Toggle: Prevents natural wind changes
        self._rain_strength = rain_strength  # Slider: Current precipitation intensity
        self._rain_locked   = rain_locked    # Toggle: Prevents natural rain changes

        # General Powers
        self._godmode       = godmode        # Player: Invulnerability status
        self._extend_range  = extend_range   # Player: Increased block placement reach
        self._spawn_rate    = spawn_rate     # Player: Enemy spawn multiplier (0.0 to 1.0)
        self._biome_spread  = biome_spread   # Toggle: Enables Corruption/Crimson/Hallow spread
        self._difficulty    = difficulty     # Slider: Enemy scaling (0.0 [0.5x] to 1.0 [3.0x])

    def __repr__(self) -> str:
        attrs = ', '.join(
            f"{k.lstrip('_')}={v!r}"
            for k, v in self.__dict__.items()
            if k.startswith('_')
        )
        return f"{self.__class__.__name__}({attrs})"

    @classmethod
    def read(cls, fr: FileReader) -> Powers:
        powers = cls()

        while fr.bool():
            power_id = fr.int2()

            match power_id:
                case PowerId.TIME_LOCKED  : powers.time_locked  = fr.bool()
                case PowerId.GODMODE      : powers.godmode      = fr.bool()
                case PowerId.TIME_RATE    : powers.time_rate    = fr.single()
                case PowerId.RAIN_LOCKED  : powers.rain_locked  = fr.bool()
                case PowerId.WIND_LOCKED  : powers.wind_locked  = fr.bool()
                case PowerId.EXTEND_RANGE : powers.extend_range = fr.bool()
                case PowerId.DIFFICULTY   : powers.difficulty   = fr.single()
                case PowerId.SPREAD_LOCKED: powers.biome_spread = not fr.bool()
                case PowerId.SPAWN_RATE   : powers.spawn_rate   = fr.single()

        return powers

    @property
    def spawn_rate(self) -> float:
        """
        The active enemy spawn multiplier.
        
        Returns:
            float: A multiplier from 0.0x (disabled) to 10.0x.
                   - 0.12x to 0.98x: Reduced spawns.
                   - 1.00x to 10.0x: Standard to chaotic spawns.
        """
        v = self._spawn_rate
        if v <= 0.0: return 0.0
        if v < 0.5:
            return round(Utils.remap(v, 0.0, 0.5, 0.1, 1.0), 2)
        return round(Utils.remap(v, 0.5, 1.0, 1.0, 10.0), 2)

    @spawn_rate.setter
    def spawn_rate(self, value: float) -> None:
        """
        Sets the spawn rate multiplier using a normalized float.
        
        Args:
            value: A float from 0.0 to 1.0.
                   - default value is 0.5 (1x).
        """
        self._spawn_rate = Math.clamp(value, 0.0, 1.0)

    @property
    def time_rate(self) -> int:
        """
        The time acceleration factor.
        
        Returns:
            int: Multiplier from 1 to 24 (e.g., 24 means 1 hour passes in 2.5 mins).
        """
        v = self._time_rate
        return int(round(Utils.remap(v, 0.0, 1.0, 1.0, 24.0)))

    @time_rate.setter
    def time_rate(self, value: float) -> None:
        """
        Sets the speed of time progression.
        
        Args:
            value: A float from 0.0 (1x speed) to 1.0 (24x speed).
                   - default value is 0.0 (1x).
        """
        self._time_rate = Math.clamp(value, 0.0, 1.0)

    @property
    def difficulty(self) -> float:
        """
        The enemy scaling and difficulty multiplier.
        
        Returns:
            float: Multiplier from 0.5x to 3.0x, snapped to 0.05 increments.
                   - 0.5x to 0.95x: Journey
                   - 1.0x to 1.95x: Classic
                   - 2.0x to 2.95x: Expert
                   - 3.0x: Master
        """
        v = self._difficulty
        if   v < 0.33: multiplier = Utils.remap(v, 0.00, 0.33, 0.5, 1.0)
        elif v < 0.66: multiplier = Utils.remap(v, 0.33, 0.66, 1.0, 2.0)
        else         : multiplier = Utils.remap(v, 0.66, 1.00, 2.0, 3.0)

        return round(math.ceil(multiplier / 0.05) * 0.05, 2)

    @difficulty.setter
    def difficulty(self, value: float) -> None:
        """
        Sets the world difficulty scaling.
        
        Args:
            value: A float from 0.0 to 1.0 mapping across all difficulty tiers.
                   - default value is 0.33 (1x - Classic Mode).
        """
        self._difficulty = Math.clamp(value, 0.0, 1.0)

    @property
    def wind_velocity(self) -> int:
        """
        The calculated wind velocity in mph.

        Returns:
            int: Velocity from -40 (Eastward) to 40 (Westward).
                 0 indicates no wind.
        """
        v = self._wind_strength
        return int(v * 50)

    @wind_velocity.setter
    def wind_velocity(self, value: float) -> None:
        """
        Sets the wind strength from a normalized float.

        Args:
            value: A float between -0.8 and 0.8.
                   - Negative values (-0.8 to -0.02) map to Eastward wind.
                   - Positive values (0.02 to 0.8) map to Westward wind.
                   - default value is 0.0 (0 - No Wind).
        """
        self._wind_strength = Math.clamp(value, -0.8, 0.8)

    @property
    def rain_intensity(self) -> int:
        """
        The current precipitation percentage and tier.
        
        Returns:
            int: Intensity from 0 to 100.
                 - Values from 0% to 39% are for Clear sky.
                 - Values from 40% to 79% are for Drizzle.
                 - Values from 80% to 100% are for Monsoon.
        """
        v = self._rain_strength
        return int(v * 100)

    @rain_intensity.setter
    def rain_intensity(self, value: float) -> None:
        """
        Sets the rain strength.
        
        Args:
            value: A float between 0.0 and 1.0.
                   - Values from (0.0 to 0.39) map to Clear sky.
                   - Values from (0.4 to 0.79) map to Drizzle.
                   - Values from (0.8 to 1.00) map to Monsoon.
                   - default value is 0.0 (0% - Clear sky).
        """
        self._rain_strength = Math.clamp(value, 0.0, 1.0)
