from dataclasses import dataclass


@dataclass
class WorldSeed:
    """Information about the world seeds."""

    def __init__(
        self,
        is_drunk: bool,
        is_not_the_bees: bool,
        is_for_the_worthy: bool,
        is_celebration_mk10: bool,
        is_the_constant: bool,
        is_remix: bool,
        is_no_traps: bool,
        is_zenith: bool,
        is_skyblock: bool,
        is_endless_halloween: bool,
        is_endless_christmas: bool,
        is_team_based_spawns: bool,
        is_dual_dungeon: bool,
    ) -> None:
        # World Seeds

        self.is_drunk: bool = is_drunk
        """If the world was created with the `Drunk <https://terraria.wiki.gg/wiki/Drunk>`_ seed."""

        self.is_not_the_bees: bool = is_not_the_bees
        """If the world was created with the `Not the Bees <https://terraria.wiki.gg/wiki/Not_the_Bees>`_ seed."""

        self.is_for_the_worthy: bool = is_for_the_worthy
        """If the world was created with the `For the Worthy <https://terraria.wiki.gg/wiki/For_the_Worthy>`_ seed."""

        self.is_celebration_mk10: bool = is_celebration_mk10
        """If the world was created with the `Celebration Mk 10 <https://terraria.wiki.gg/wiki/Celebration_Mk_10>` seed."""

        self.is_the_constant: bool = is_the_constant
        """If the world was created with `The Constant <https://terraria.wiki.gg/wiki/The_Constant>`_ seed."""

        self.is_remix: bool = is_remix  # AKA "Don't Dig Up"
        """If the world was created with the `Remix <https://terraria.wiki.gg/wiki/Remix>`_ seed."""

        self.is_no_traps: bool = is_no_traps
        """If the world was created with the `No Traps <https://terraria.wiki.gg/wiki/No_Traps>`_ seed."""

        self.is_zenith: bool = is_zenith  # AKA "Get Fixed Boi"
        """If the world was created with the `Zenith <https://terraria.wiki.gg/wiki/Get_fixed_boi>`_ seed."""

        self.is_skyblock: bool = is_skyblock
        """If the world was created with the `Skyblock <https://terraria.wiki.gg/wiki/Skyblock>`_ seed."""

        # Secret World Seeds

        self.is_endless_halloween: bool = is_endless_halloween  # AKA "Hocus Pocus"
        """If the world was created with the `Endless Halloween <https://terraria.wiki.gg/wiki/Secret_world_seeds#endlessHalloween>`_ seed."""

        self.is_endless_christmas: bool = (
            is_endless_christmas  # AKA "Jingle all the Way"
        )
        """If the world was created with the `Endless Christmas <https://terraria.wiki.gg/wiki/Secret_world_seeds#endlessChristmas>`_ seed."""

        self.is_team_based_spawns: bool = (
            is_team_based_spawns  # AKA "Royal with Cheese"
        )
        """If the world was created with the `Team based spawns <https://terraria.wiki.gg/wiki/Secret_world_seeds#teamBasedSpawns>`_ seed."""

        self.is_dual_dungeon: bool = is_dual_dungeon
        """If the world was created with the `Dual Dungeons <https://terraria.wiki.gg/wiki/Secret_world_seeds#dualDungeons>`_ seed."""

    @property
    def is_legendary(self) -> bool:
        return self.is_for_the_worthy or self.is_zenith
