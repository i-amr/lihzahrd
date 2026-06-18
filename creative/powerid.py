import enum


class PowerId(enum.IntEnum):
    # Time Section
    TIME_LOCKED   = 0  # FreezeTime                     `time_setfrozen`
    SET_DAWN      = 1  # StartDayImmediately            `time_setdawn`     04:30 AM
    SET_NOON      = 2  # StartNoonImmediately           `time_setnoon`     12:00 PM
    SET_DUSK      = 3  # StartNightImmediately          `time_setdusk`     07:30 PM
    SET_MOON      = 4  # StartMidnightImmediately       `time_setmidnight` 12:00 AM
    TIME_RATE     = 8  # ModifyTimeRate                 `time_setspeed`

    # Weather Section
    WIND_STRENGTH = 6  # ModifyWindDirectionAndStrength `wind_setstrength`
    WIND_LOCKED   = 10 # FreezeWindDirectionAndStrength `wind_setfrozen`
    RAIN_STRENGTH = 7  # ModifyRainPower                `rain_setstrength`
    RAIN_LOCKED   = 9  # FreezeRainPower                `rain_setfrozen`

    # Powers Section
    GODMODE       = 5  # GodmodePower                   `godmode`
    EXTEND_RANGE  = 11 # FarPlacementRangePower         `increaseplacementrange`
    SPAWN_RATE    = 14 # SpawnRateSliderPerPlayerPower  `setspawnrate`
    SPREAD_LOCKED = 13 # StopBiomeSpreadPower           `biomespread_setfrozen`
    DIFFICULTY    = 12 # DifficultySliderPower          `setdifficulty`
