import os
import sys
import uuid
import struct
import numpy as np

from datetime import datetime
from PIL import Image, ImageDraw
from contextlib import contextmanager

from typing import *
from .fileutils import *
from .data import *
from .enums import *
from .items import *
from .header import *
from .tiles import *
from .bestiary import *
from .creative import *
from .chests import *
from .signs import *
from .npcs import *
from .tileentities import *
from .pressureplates import *
from .townmanager import *
from .errors import *
from .metadata import Metadata
from .footer import Footer
from .export import Renderer
from .fileutils import NetDateTime as ndt


class World:
    """The Python representation of a Terraria world."""

    min_version = Version(269)
    max_version = Version(318)

    def __init__(self, data, verbose: bool = False):
        if not isinstance(data, str) and not (hasattr(data, 'read') and callable(data.read)):
            raise TypeError(f"Expected file path or stream, got {type(data).__name__}")

        if isinstance(data, str) and not os.path.exists(data):
            raise FileNotFoundError(f"File not found: {data}")

        with FileReader(data) as fr:
            self._verbose = verbose
            self.__load_world(fr)

    def __repr__(self):
        return f'<World "{self.label}">'

    @property
    def crimson_hearts(self) -> ShadowOrbs:
        """Information related to the Shadow Orbs or Crimson Hearts in the world."""
        return self.shadow_orbs

    @crimson_hearts.setter
    def crimson_hearts(self, value):
        self.shadow_orbs = value

    @property
    def is_classic(self):
        """If the world is in classic difficulty or not."""
        return self.difficulty == Difficulty.CLASSIC

    @property
    def is_expert(self):
        """If the world is in expert difficulty or not."""
        return (
            self.difficulty == Difficulty.EXPERT
            or self.difficulty == Difficulty.CLASSIC
            and self.world_seed.is_legendary()
        )

    @property
    def is_master(self):
        """If the world is in master difficulty or not."""
        return (
            self.difficulty == Difficulty.MASTER
            or self.difficulty == Difficulty.EXPERT
            and self.world_seed.is_legendary()
        )

    @property
    def is_legendary(self):
        """If the world is in legendary difficulty or not."""
        return (
            self.difficulty == Difficulty.MASTER and self.world_seed.is_legendary()
        )

    @property
    def is_journey(self):
        """If the world is in journey difficulty or not."""
        return self.difficulty == 3

    def render(
        self,
        output_file: str = None,
        draw_background: bool = True,
        draw_blocks: bool = True,
        draw_walls: bool = True,
        draw_paint: bool = True,
        draw_liquids: bool = True,
        draw_wires: bool = False,
    ):
        Renderer.export(
            size=self.size,
            tiles=self.tiles,
            layers=self.layers,
            output_file=output_file or f"{self.label}.png",
            draw_walls=draw_walls,
            draw_paint=draw_paint,
            draw_wires=draw_wires,
            draw_blocks=draw_blocks,
            draw_liquids=draw_liquids,
            draw_background=draw_background,
        )

    @contextmanager
    def section_guard(self, idx, fr):
        expected_pos = self._pointers[idx] if idx != 0 else 0

        if fr.tell() != expected_pos:
            raise SectionError(
                f"Bad Section Pointer at index {idx}! "
                f"Expected {expected_pos}, got {fr.tell()}"
            )

        yield

        if self._verbose:
            print(f"Section {idx} loaded successfully.")

    def __load_world(self, fr: FileReader) -> int:
        with self.section_guard(0, fr):
            self.__load_file_format_header(fr)

        with self.section_guard(1, fr):
            self.__load_header(fr)

        with self.section_guard(2, fr):
            self.__load_world_tiles(fr)

        with self.section_guard(3, fr):
            self.__load_chests(fr)

        with self.section_guard(4, fr):
            self.__load_signs(fr)

        with self.section_guard(5, fr):
            self.__load_npcs(fr)

        with self.section_guard(6, fr):
            self.__load_tile_entities(fr)

        with self.section_guard(7, fr):
            self.__load_weighted_pressure_plates(fr)

        with self.section_guard(8, fr):
            self.__load_town_manager(fr)

        with self.section_guard(9, fr):
            self.__load_bestiary(fr)

        with self.section_guard(10, fr):
            self.__load_creative_powers(fr)

        return self.__load_footer(fr)

    def __load_file_format_header(self, fr: FileReader) -> bool:
        self.version = Version(fr.int4())

        if not (self.min_version <= self.version <= self.max_version):
            raise UnsupportedVersionError(
                f"World version {self.version.id} is not supported.\n"
                f"This library is strictly tuned for versions {self.min_version} to {self.max_version}.\n"
                f"Please provide a compatible world file from Terraria 1.4.4+."
            )

        self.metadata = Metadata.read(fr, expected_type=FileType.WORLD)

        self._pointers = Pointers(*[fr.int4() for _ in range(fr.int2())])
        importance = []
        for _ in range((fr.int2() + 7) // 8):
            importance = [*importance, *fr.bits()]

        self._importance = importance

    def __load_header(self, fr: FileReader) -> None:
        v = self.version

        self.label = fr.string()

        self.generator = GeneratorInfo(fr.string(), fr.uint8())

        self.uid = fr.uuid()  # for setter uuid.uuid4() would work
        self.id = fr.int4()

        self.bounds = fr.rect()

        self.size = Dimensions(h=fr.int4(), w=fr.int4())

        self.difficulty = Difficulty(fr.int4())

        is_drunk_world = fr.bool()
        is_for_the_worthy = fr.bool()
        is_tenth_anniversary = fr.bool()
        is_the_constant = fr.bool()
        is_bee_world = fr.bool()
        is_upside_down = fr.bool()
        is_trap_world = fr.bool()
        is_zenith_world = fr.bool()
        is_skyblock_world = v >= Version(302) and fr.bool()

        self.created_at = ndt.bin(fr.uint8())
        if v >= Version(284):
            self.last_played = ndt.bin(fr.uint8())
        else:
            self.last_played = ndt.bin(ndt.bin())

        moon_style = fr.uint1()

        trees_separators = [fr.int4(), fr.int4(), fr.int4()]
        trees_properties = [fr.int4(), fr.int4(), fr.int4(), fr.int4()]

        moss_separators = [fr.int4(), fr.int4(), fr.int4()]
        moss_properties = [fr.int4(), fr.int4(), fr.int4(), fr.int4()]

        tundra_background_style = fr.int4()
        jungle_background_style = fr.int4()
        hell_background_style = fr.int4()

        spawn_point = Coordinates(fr.int4(), fr.int4())

        self.layers = Layers(
            surface=fr.double(),
            underground=fr.double(),
            hell=float(self.size.h),
        )

        current_time = fr.double()
        is_daytime = fr.bool()
        moon_phase = MoonPhase(fr.uint4())

        is_blood_moon = fr.bool()
        is_eclipse = fr.bool()

        dungeon_point = Coordinates(fr.int4(), fr.int4())
        world_evil = WorldEvilType(fr.bool())

        defeated_eye_of_cthulhu = fr.bool()
        defeated_eater_of_worlds = fr.bool()
        defeated_skeletron = fr.bool()
        defeated_queen_bee = fr.bool()
        defeated_the_destroyer = fr.bool()
        defeated_the_twins = fr.bool()
        defeated_skeletron_prime = fr.bool()
        defeated_any_mechnical_boss = fr.bool()
        defeated_plantera = fr.bool()
        defeated_golem = fr.bool()
        defeated_king_slime = fr.bool()

        saved_goblin_tinkerer = fr.bool()
        saved_wizard = fr.bool()
        saved_mechanic = fr.bool()

        defeated_goblin_army = fr.bool()
        defeated_clown = fr.bool()
        defeated_frost_moon = fr.bool()
        defeated_pirate_invasion = fr.bool()

        shadow_orb_smashed = fr.bool()
        spawn_meteorite = fr.bool()
        shadow_orb_count = fr.uint1()

        altar_count = fr.int4()

        is_hardmode = fr.bool()

        party_is_doomed = fr.bool()

        invasion_delay = fr.int4()
        invasion_size = fr.int4()
        invasion_type = InvasionType(fr.int4())
        invasion_x = fr.double()

        slime_rain_time_left = fr.double()

        sundial_cooldown = fr.uint1()

        is_raining = fr.bool()
        rain_time_left = fr.int4()
        max_rain = fr.single()

        ore_tier_5 = BlockType(fr.int4())  # cobalt     or palladium
        ore_tier_6 = BlockType(fr.int4())  # mythril    or orichalcum
        ore_tier_7 = BlockType(fr.int4())  # adamantite or titanium

        bg_forest = fr.uint1()
        bg_corruption = fr.uint1()
        bg_jungle = fr.uint1()
        bg_tundra = fr.uint1()
        bg_hallow = fr.uint1()
        bg_crimson = fr.uint1()
        bg_desert = fr.uint1()
        bg_ocean = fr.uint1()

        active_cloud_background = fr.int4()
        opacity_cloud_background = 0.0 if active_cloud_background < 1 else 1.0
        cloud_number = fr.int2()
        wind_speed = fr.single()

        angler_who_finished_today = [fr.string() for _ in range(fr.int4())]
        saved_angler = fr.bool()
        angler_today_quest = AnglerQuestFish(fr.int4())

        saved_stylist = fr.bool()
        saved_tax_collector = fr.bool()
        saved_golfer = fr.bool()

        invasion_size_start = fr.int4()

        cultist_delay = fr.int4()

        mob_kills = [fr.int4() for _ in range(fr.int2())]

        if v >= Version(289):
            claimable_banners = [fr.uint2() for _ in range(fr.int2())]
        else:
            claimable_banners = []

        sundial_is_running = fr.bool()

        defeated_duke_fishron = fr.bool()
        defeated_martian_madness = fr.bool()
        defeated_lunatic_cultist = fr.bool()
        defeated_moon_lord = fr.bool()
        defeated_pumpking = fr.bool()
        defeated_mourning_wood = fr.bool()
        defeated_ice_queen = fr.bool()
        defeated_santa_nk1 = fr.bool()
        defeated_everscream = fr.bool()

        defeated_solar_pillar = fr.bool()
        defeated_vortex_pillar = fr.bool()
        defeated_nebula_pillar = fr.bool()
        defeated_stardust_pillar = fr.bool()

        active_solar_pillar = fr.bool()
        active_vortex_pillar = fr.bool()
        active_nebula_pillar = fr.bool()
        active_stardust_pillar = fr.bool()

        active_lunar_apocalypse = fr.bool()

        party_center_active = fr.bool()
        party_natural_active = fr.bool()
        party_cooldown = fr.int4()
        partying_npcs = [fr.int4() for _ in range(fr.int4())]

        sandstorm_active = fr.bool()
        sandstorm_time_left = fr.int4()
        sandstorm_severity = fr.single()
        sandstorm_intended_severity = fr.single()

        saved_bartender = fr.bool()
        old_ones_army = OldOnesArmyTiers(fr.bool(), fr.bool(), fr.bool())

        bg_mushroom = fr.uint1()
        bg_underworld = fr.uint1()

        bg_forest_2 = fr.uint1()
        bg_forest_3 = fr.uint1()
        bg_forest_4 = fr.uint1()

        combat_book_used = fr.bool()

        lantern_night_cooldown = fr.int4()
        lantern_night_natural = fr.bool()
        lantern_night_manual = fr.bool()
        next_night_is_lantern_night = fr.bool()

        treetop_variants = TreetopVariants([fr.int4() for _ in range(fr.int4())])

        is_halloween = fr.bool()
        is_christmas = fr.bool()

        ore_tier_1 = BlockType(fr.int4())  # copper or tin
        ore_tier_2 = BlockType(fr.int4())  # iron   or lead
        ore_tier_3 = BlockType(fr.int4())  # silver or tungsten
        ore_tier_4 = BlockType(fr.int4())  # gold   or platinum

        cat = fr.bool()
        dog = fr.bool()
        bunny = fr.bool()

        defeated_empress_of_light = fr.bool()
        defeated_queen_slime = fr.bool()

        defeated_deerclops = fr.bool()

        saved_slime_nerdy = fr.bool()

        saved_merchant = fr.bool()
        saved_demolitionist = fr.bool()
        saved_party_girl = fr.bool()
        saved_dye_trader = fr.bool()
        saved_truffle = fr.bool()
        saved_arms_dealer = fr.bool()
        saved_nurse = fr.bool()
        saved_princess = fr.bool()

        combat_book_2_used = fr.bool()
        peddler_satchel_used = fr.bool()

        saved_slime_cool = fr.bool()
        saved_slime_elder = fr.bool()
        saved_slime_clumsy = fr.bool()
        saved_slime_diva = fr.bool()
        saved_slime_surly = fr.bool()
        saved_slime_mystic = fr.bool()
        saved_slime_squire = fr.bool()

        moondial_is_running = fr.bool()
        moondial_cooldown = fr.uint1()

        is_endless_halloween = v >= Version(287) and fr.bool()
        is_endless_christmas = v >= Version(287) and fr.bool()

        is_vampire_world  = v >= Version(288) and fr.bool()
        is_infected_world = v >= Version(296) and fr.bool()

        if v >= Version(291):
            meteor_shower_count = fr.int4()
            coins_rain = fr.int4()
        else:
            meteor_shower_count = 0
            coins_rain = 0

        if v >= Version(297):
            is_team_based_spawns = fr.bool()
            team_count = fr.uint1()
            team_spawn = [Coordinates(x=fr.int2(), y=fr.int2()) for _ in range(team_count)]
        else:
            is_team_based_spawns = False
            team_count = 0
            team_spawn = []

        is_dual_dungeon = v >= Version(304) and fr.bool()

        if v >= Version(299):
            if v <= Version(312):
                internal_version = fr.uint4()
            manifest = fr.string()

        self.world_seed = WorldSeed(
            is_drunk=is_drunk_world,
            is_not_the_bees=is_bee_world,
            is_for_the_worthy=is_for_the_worthy,
            is_celebration_mk10=is_tenth_anniversary,
            is_the_constant=is_the_constant,
            is_remix=is_upside_down,
            is_no_traps=is_trap_world,
            is_zenith=is_zenith_world,
            is_skyblock=is_skyblock_world,
            is_endless_halloween=is_endless_halloween,
            is_endless_christmas=is_endless_christmas,
            is_team_based_spawns=is_team_based_spawns,
            is_dual_dungeon=is_dual_dungeon,
        )

        self.world_styles = Styles(
            moon=MoonStyle(moon_style),
            trees=FourPartSplit(
                separators=trees_separators,
                properties=trees_properties,
            ),
            moss=FourPartSplit(
                separators=moss_separators,
                properties=moss_properties,
            ),
        )

        self.shadow_orbs = ShadowOrbs(
            smashed_at_least_once=shadow_orb_smashed,
            spawn_meteorite=spawn_meteorite,
            evil_boss_counter=shadow_orb_count,
        )

        self.rain = Rain(
            is_active=is_raining,
            time_left=rain_time_left,
            max_rain=max_rain,
        )

        self.clouds = Clouds(
            is_active=active_cloud_background,
            cloud_number=cloud_number,
            wind_speed=wind_speed,
        )

        self.anglers_quest = AnglerQuest(
            current_goal=angler_today_quest,
            completed_by=angler_who_finished_today,
        )

        self.invasion = Invasion(
            delay=invasion_delay,
            size=invasion_size,
            type_=invasion_type,
            position=invasion_x,
            size_start=invasion_size_start,
        )

        self.defeated_pillars = PillarsInfo(
            solar=defeated_solar_pillar,
            vortex=defeated_vortex_pillar,
            nebula=defeated_nebula_pillar,
            stardust=defeated_stardust_pillar,
        )

        self.lunar_events = LunarEvents(
            pillars_present=PillarsInfo(
                solar=active_solar_pillar,
                vortex=active_vortex_pillar,
                nebula=active_nebula_pillar,
                stardust=active_stardust_pillar,
            ),
            apocalypse=active_lunar_apocalypse,
        )

        self.party = Party(
            is_doomed=party_is_doomed,
            cooldown=party_cooldown,
            natural=party_natural_active,
            manual=party_center_active,
            partying_npcs=partying_npcs,
        )

        self.sandstorm = Sandstorm(
            is_active=sandstorm_active,
            time_left=sandstorm_time_left,
            severity=sandstorm_severity,
            intended_severity=sandstorm_intended_severity,
        )

        self.backgrounds = Backgrounds(
            underground_tundra=tundra_background_style,
            underground_jungle=jungle_background_style,
            hell=hell_background_style,
            forest=FourPartSplit(
                self.world_styles.trees.separators,
                [bg_forest, bg_forest_2, bg_forest_3, bg_forest_4],
            ),
            corruption=bg_corruption,
            jungle=bg_jungle,
            tundra=bg_tundra,
            hallow=bg_hallow,
            crimson=bg_crimson,
            desert=bg_desert,
            ocean=bg_ocean,
            mushroom=bg_mushroom,
            underworld=bg_underworld,
        )

        self.lantern_night = LanternNight(
            cooldown=lantern_night_cooldown,
            natural=lantern_night_natural,
            manual=lantern_night_manual,
            next_night_is_lantern_night=next_night_is_lantern_night,
        )

        self.events = Events(
            is_blood_moon=is_blood_moon,
            is_solar_eclipse=is_eclipse,
            is_halloween=is_halloween,
            is_christmas=is_christmas,
            invasion=self.invasion,
            slime_rain=slime_rain_time_left,
            rain=self.rain,
            party=self.party,
            sandstorm=self.sandstorm,
            lunar_events=self.lunar_events,
            lantern_night=self.lantern_night,
        )

        self.pets = Pets(
            cat=cat,
            dog=dog,
            bunny=bunny,
        )

        self.saved_ore_tiers = SavedOreTiers(
            tier_1=ore_tier_1,
            tier_2=ore_tier_2,
            tier_3=ore_tier_3,
            tier_4=ore_tier_4,
            tier_5=ore_tier_5,
            tier_6=ore_tier_6,
            tier_7=ore_tier_7,
        )

        self.bosses_defeated = BossesDefeated(
            eye_of_cthulhu=defeated_eye_of_cthulhu,
            eater_of_worlds=defeated_eater_of_worlds,
            skeletron=defeated_skeletron,
            queen_bee=defeated_queen_bee,
            the_twins=defeated_the_twins,
            the_destroyer=defeated_the_destroyer,
            skeletron_prime=defeated_skeletron_prime,
            any_mechnical_boss=defeated_any_mechnical_boss,
            plantera=defeated_plantera,
            golem=defeated_golem,
            king_slime=defeated_king_slime,
            goblin_army=defeated_goblin_army,
            clown=defeated_clown,
            frost_moon=defeated_frost_moon,
            pirates=defeated_pirate_invasion,
            duke_fishron=defeated_duke_fishron,
            moon_lord=defeated_moon_lord,
            pumpking=defeated_pumpking,
            mourning_wood=defeated_mourning_wood,
            ice_queen=defeated_ice_queen,
            santa_nk1=defeated_santa_nk1,
            everscream=defeated_everscream,
            lunar_pillars=self.defeated_pillars,
            old_ones_army=old_ones_army,
            martian_madness=defeated_martian_madness,
            lunatic_cultist=defeated_lunatic_cultist,
            empress_of_light=defeated_empress_of_light,
            queen_slime=defeated_queen_slime,
            deerclops=defeated_deerclops,
        )

        self.saved_npcs = SavedNPCs(
            goblin_tinkerer=saved_goblin_tinkerer,
            wizard=saved_wizard,
            mechanic=saved_mechanic,
            angler=saved_angler,
            stylist=saved_stylist,
            tax_collector=saved_tax_collector,
            bartender=saved_bartender,
            golfer=saved_golfer,
            advanced_combat=combat_book_used,
            slime_nerdy=saved_slime_nerdy,
            merchant=saved_merchant,
            demolitionist=saved_demolitionist,
            party_girl=saved_party_girl,
            dye_trader=saved_dye_trader,
            truffle=saved_truffle,
            arms_dealer=saved_arms_dealer,
            nurse=saved_nurse,
            princess=saved_princess,
            advanced_combat_2=combat_book_2_used,
            peddlers_satchel=peddler_satchel_used,
            slime_cool=saved_slime_cool,
            slime_elder=saved_slime_elder,
            slime_clumsy=saved_slime_clumsy,
            slime_diva=saved_slime_diva,
            slime_surly=saved_slime_surly,
            slime_mystic=saved_slime_mystic,
            slime_squire=saved_slime_squire,
        )

        self.time = Time(
            current=current_time,
            is_daytime=is_daytime,
            moon_phase=moon_phase,
            sundial_cooldown=sundial_cooldown,
            sundial_is_running=sundial_is_running,
            moondial_cooldown=moondial_cooldown,
            moondial_is_running=moondial_is_running,
        )

    @staticmethod
    def __read_tile_block(fr: FileReader, importance: list[bool]) -> tuple[Tile, int]:
        # Read flag bytes
        flags1 = fr.uint1()
        flags2 = fr.uint1() if flags1 & 0x01 else 0
        flags3 = fr.uint1() if flags2 & 0x01 else 0
        flags4 = fr.uint1() if flags3 & 0x01 else 0

        # Parse flags1
        has_block = bool(flags1 & 0x02)
        has_wall = bool(flags1 & 0x04)
        liquid_bits = (flags1 & 0x18) >> 3  # bits 3-4
        has_extended_block_id = bool(flags1 & 0x20)
        rle_bits = (flags1 & 0xC0) >> 6  # bits 6-7

        # Parse flags2
        if flags2 > 1:  # flags1 & 0x01:
            has_red_wire = bool(flags2 & 0x02)
            has_blue_wire = bool(flags2 & 0x04)
            has_green_wire = bool(flags2 & 0x08)
            block_shape = Shape((flags2 & 0x70) >> 4)  # bits 4-6
        else:
            has_red_wire = False
            has_blue_wire = False
            has_green_wire = False
            block_shape = Shape.NORMAL

        # Parse flags3
        if flags3 > 1:  # flags3:
            has_actuator = bool(flags3 & 0x02)
            is_block_active = not (flags3 & 0x04)
            is_painted_block = bool(flags3 & 0x08)
            has_wall_paint = bool(flags3 & 0x10)
            has_yellow_wire = bool(flags3 & 0x20)
            has_extended_wall_id = bool(flags3 & 0x40)
            is_shimmer = bool(flags3 & 0x80)
        else:
            has_yellow_wire = False
            is_block_active = True
            is_painted_block = False
            has_wall_paint = False
            has_actuator = False
            has_extended_wall_id = False
            is_shimmer = False

        wiring = Wiring(
            red=has_red_wire,
            green=has_green_wire,
            blue=has_blue_wire,
            yellow=has_yellow_wire,
            actuator=has_actuator,
        )

        # Parse flags4
        if flags4 > 1:  # flags4:
            is_echo_block = bool(flags4 & 0x02)
            is_echo_wall = bool(flags4 & 0x04)
            is_illuminant_block = bool(flags4 & 0x08)
            is_illuminant_wall = bool(flags4 & 0x10)
        else:
            is_echo_block = False
            is_echo_wall = False
            is_illuminant_block = False
            is_illuminant_wall = False

        # Read block data
        if has_block:
            if has_extended_block_id:
                block_low = fr.uint1()
                block_high = fr.uint1()
                tile_type = (block_high << 8) | block_low
            else:
                tile_type = fr.uint1()

            # Check if this tile type has frame data
            tile_frame = None
            if importance[tile_type]:
                tile_frame = FrameImportantData(fr.int2(), fr.int2())
                if tile_type == 144:
                    tile_frame.y = 0

            # Read block paint if flag is set
            tile_block_paint = fr.uint1() if is_painted_block else None

            block = Block(
                type_=BlockType(tile_type),
                frame=tile_frame,
                paint=tile_block_paint,
                is_active=is_block_active,  # always True!
                shape=block_shape,
                is_illuminant=is_illuminant_block,
                is_echo=is_echo_block,
            )
        else: block = None

        # Read wall data (first byte)
        wall = Wall(
            type_=WallType(0),
            is_illuminant=is_illuminant_wall,
            is_echo=is_echo_wall,
        )
        if has_wall:
            wall.type = WallType(fr.uint1())

            # Read wall paint if flag is set
            wall.paint = fr.uint1() if has_wall_paint else None

        # Read liquid data
        if liquid_bits:
            tile_liquid_amount = fr.uint1()

            tile_liquid_type = LiquidType.SHIMMER if is_shimmer else LiquidType(liquid_bits)

            liquid = Liquid(
                type_=tile_liquid_type,
                volume=tile_liquid_amount,
            )
        else: liquid = None

        # Read extended wall ID (high byte)
        if has_extended_wall_id:
            wall_high = fr.uint1()
            wall.type = WallType((wall_high << 8) | wall.type)

        # Read RLE count
        rle = 0
        match rle_bits:
            case RLEEncoding.NO_COMPRESSION:
                rle = 0
            case RLEEncoding.SINGLE_BYTE:
                rle = fr.uint1()
            case RLEEncoding.DOUBLE_BYTE:
                rle = fr.int2()
            case _:
                rle = fr.int2()

        tile = Tile(
            block=block,
            wall=wall,
            liquid=liquid,
            wiring=wiring,
        )

        return tile, rle

    def __load_world_tiles(self, fr: FileReader) -> None:
        tm = TileMatrix()
        importance = self._importance
        w, h = self.size.w, self.size.h

        for x in range(w):
            y = 0
            column = []

            while y < h:
                tile, rle = self.__read_tile_block(fr, importance)

                count = rle + 1

                if y + count > h:
                    count = h - y

                column.extend([tile] * count)

                y += count

            tm.add_column(column)

        self.tiles = tm

    def __load_chests(self, fr: FileReader) -> None:
        v = self.version

        chests: list[Chest] = []
        chests_count = fr.int2()
        items_per_chest = fr.int2() if v < Version(294) else 0

        for _ in range(chests_count):
            chest = Chest.read(fr, v, items_per_chest)
            chests.append(chest)
            self.tiles[chest.position].extra = chest

        self.chests = chests

    def __load_signs(self, fr: FileReader) -> None:
        signs: list[Sign] = []
        signs_count = fr.int2()

        for _ in range(signs_count):
            sign = Sign.read(fr)
            signs.append(sign)
            self.tiles[sign.position].extra = sign

        self.signs = signs

    def __load_npcs(self, fr: FileReader) -> None:
        v = self.version

        shimmered_npcs: list[int] = []
        shimmered_npcs_count = fr.int4()
        for _ in range(shimmered_npcs_count):
            shimmered_npcs.append(fr.int4())
        self.shimmered_npcs = shimmered_npcs

        npcs: list[NPC] = []
        while fr.bool():
            npc = NPC.read(fr, v)
            npcs.append(npc)
        self.npcs = npcs

        mobs: list[Mob] = []
        while fr.bool():
            mob = Mob.read(fr)
            mobs.append(mob)
        self.mobs = mobs

    def __load_tile_entities(self, fr: FileReader) -> None:
        v = self.version
        tile_entities_count = fr.int4()
        tile_entities = []

        for _ in range(tile_entities_count):
            tile_entity = TileEntity.read(fr, v)
            tile_entities.append(tile_entity)
            if tile_entity.position >= Coordinates(0, 0) and tile_entity.position <= self.tiles.size:
                self.tiles[tile_entity.position].extra = tile_entity

        self.tile_entities = tile_entities

    def __load_weighted_pressure_plates(self, fr: FileReader) -> None:
        pressure_plates_count = fr.int4()
        pressure_plates = []

        for _ in range(pressure_plates_count):
            pressure_plate = WeighedPressurePlate.read(fr)
            pressure_plates.append(pressure_plate)
            self.tiles[pressure_plate.position].extra = pressure_plate

        self.pressure_plates = pressure_plates

    def __load_town_manager(self, fr: FileReader) -> None:
        rooms_count = fr.int4()
        rooms = []

        for _ in range(rooms_count):
            room = Room.read(fr)
            rooms.append(room)

        self.rooms = rooms

    def __load_bestiary(self, fr: FileReader) -> None:
        self.bestiary = Bestiary.read(fr)

    def __load_creative_powers(self, fr: FileReader) -> None:
        self.creative_powers = Powers.read(fr)

        self.creative_powers.rain_intensity = self.rain.max_rain
        self.creative_powers.wind_velocity  = self.clouds.wind_speed

    def __load_footer(self, fr: FileReader) -> None:
        Footer.read(fr, self.label, self.id)


if __name__ == "__main__":
    world = World(sys.argv[1])
    breakpoint()

    # print(f'Creation Time: {world.created_at:%m/%d/%Y %H:%M:%S}')
    # print(f'Last Played: {world.last_played:%m/%d/%Y %H:%M:%S}')
    # print()
    # print(f'UUID: {uid}')
    # print()
