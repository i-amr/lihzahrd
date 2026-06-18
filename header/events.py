from .invasion import Invasion
from .rain import Rain
from .party import Party
from .sandstorm import Sandstorm
from .lunarevents import LunarEvents
from .lanternnight import LanternNight


class Events:
    """Information about the ongoing world events."""

    def __init__(
        self,
        is_blood_moon: bool,
        is_solar_eclipse: bool,
        is_halloween: bool,
        is_christmas: bool,
        invasion: Invasion,
        slime_rain: float,
        rain: Rain,
        party: Party,
        sandstorm: Sandstorm,
        lunar_events: LunarEvents,
        lantern_night: LanternNight,
        # coins_rain: CoinsRain,
        # meteor_shower: MeteorShower,
    ):
        self.is_blood_moon: bool = is_blood_moon
        """If the current moon is a Blood Moon."""

        self.is_solar_eclipse: bool = is_solar_eclipse
        """If the current day is a Solar Eclipse."""

        self.is_halloween: bool = is_halloween
        """Is today an Halloween reward day?
        Triggered by reaching Wave 15 of the Pumpkin Moon."""

        self.is_christmas: bool = is_christmas
        """Is today a Xmas reward day?
        Triggered by reaching Wave 20 of the Frost Moon."""

        self.invasion: Invasion = invasion
        """Information about the currently ongoing invasion."""

        self.slime_rain: float = slime_rain
        """How long the slime rain will go on for."""

        self.rain: Rain = rain
        """Information about the currently ongoing rain."""

        self.party: Party = party
        """Information about the currently ongoing party."""

        self.sandstorm: Sandstorm = sandstorm
        """Information about the currently ongoing sandstorm."""

        self.lunar_events: LunarEvents = lunar_events
        """Information about the currently ongoing Lunar Events."""

        self.lantern_night: LanternNight = lantern_night
        """Information about the currently ongoing lantern night."""

    def __repr__(self):
        return f"<WorldEvents>"
