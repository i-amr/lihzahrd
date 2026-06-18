from datetime import datetime
from PIL import Image, ImageDraw
from .color_registry import ColorRegistry
from ..data import Layers
from ..enums import LayerType, WireType
from ..fileutils import Dimensions
from ..utility import Math, Utils


class Renderer:

    @classmethod
    def export(
        cls,
        tiles,
        size: Dimensions,
        layers: Layers,
        output_file: str,
        draw_background: bool = True,
        draw_blocks: bool = True,
        draw_walls: bool = True,
        draw_paint: bool = False,
        draw_liquids: bool = True,
        draw_wires: bool = False,
    ):
        width, height = size.w, size.h

        background = cls.draw_background(layers, width, height) if draw_background else Image.new("RGBA", (width, height), (0, 0, 0, 0))
        wall_layer, block_layer, liquid_layer = cls.draw_tiles(tiles, width, height, draw_walls, draw_blocks, draw_liquids, draw_paint, draw_wires)

        print("Merging layers...")
        final = background
        final.paste(wall_layer, (0, 0), wall_layer)
        final.paste(liquid_layer, (0, 0), liquid_layer)
        final.paste(block_layer, (0, 0), block_layer)

        print("Saving image...")
        final.save(output_file)

    @classmethod
    def draw_background(cls, layers: Layers, width: int, height: int) -> Image.Image:
        background = Image.new("RGBA", (width, height))
        draw = ImageDraw.Draw(background)
        min_y = 0

        # SKY & SURFACE
        if min_y < layers.surface:
            sky_start_y = 0
            sky_end_y = min(height, int(layers.surface))
            sky_colors = ColorRegistry.LAYERS[LayerType.SPACE]
            full_grad = Utils.linear_gradient(sky_colors["start"], sky_colors["end"], count=16)

            for screen_y in range(sky_start_y, sky_end_y):
                t = screen_y / layers.surface
                color_idx = int(t * 15)
                draw.line([(0, screen_y), (width, screen_y)], fill=full_grad[color_idx])

        # UNDERGROUND
        if height > layers.surface and min_y < layers.underground:
            cls._draw_solid_layer(draw, width, height, layers.surface, layers.underground, LayerType.UNDERGROUND)

        # CAVERN
        if height > layers.underground and min_y < layers.cavern:
            cls._draw_solid_layer(draw, width, height, layers.underground, layers.cavern, LayerType.CAVERN)

        # UNDERWORLD
        if height > layers.cavern and min_y < layers.hell:
            hell_colors = ColorRegistry.LAYERS[LayerType.UNDERWORLD]
            draw.rectangle([(0, int(layers.cavern)), (width, height)], fill=hell_colors["solid"])

        del draw
        return background

    @staticmethod
    def _draw_solid_layer(draw, width, height, start_y, end_y, layer_type):
        colors = ColorRegistry.LAYERS[layer_type]
        draw.rectangle(
            [(0, int(start_y)), (width, min(height, int(end_y)))],
            fill=colors["solid"]
        )

    @classmethod
    def draw_tiles(cls, tiles, width, height, draw_walls, draw_blocks, draw_liquids, draw_paint, draw_wires):
        wall_layer   = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        block_layer  = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        liquid_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))

        wall_pixels   = wall_layer.load()
        block_pixels  = block_layer.load()
        liquid_pixels = liquid_layer.load()

        start_time = datetime.now().timestamp()

        for x in range(width):
            for y in range(height):
                tile = tiles[x, y]

                if draw_walls and tile.wall:
                    wall_pixels[x, y] = (
                        ColorRegistry.PAINTS[tile.wall.paint]
                        if draw_paint and tile.wall.paint
                        else ColorRegistry.WALLS[tile.wall.type]
                    )

                if draw_liquids and tile.liquid:
                    liquid_pixels[x, y] = ColorRegistry.LIQUIDS[tile.liquid.type]

                if draw_blocks and tile.block:
                    block_pixels[x, y] = (
                        ColorRegistry.PAINTS[tile.block.paint]
                        if draw_paint and tile.block.paint
                        else ColorRegistry.BLOCKS[tile.block.type]
                    )

                if draw_wires and tile.wiring:
                    for wire_type, has_wire in [
                        (WireType.RED,    tile.wiring.red),
                        (WireType.BLUE,   tile.wiring.blue),
                        (WireType.GREEN,  tile.wiring.green),
                        (WireType.YELLOW, tile.wiring.yellow),
                    ]:
                        if has_wire:
                            block_pixels[x, y] = ColorRegistry.WIRES[wire_type]
                            break

            if x % 500 == 0 and x > 0:
                elapsed = datetime.now().timestamp() - start_time
                progress = x / width
                remaining = (elapsed / progress) - elapsed
                print(f"Column {x}/{width} ({progress:.1%}) - Est. Remaining: {remaining:.1f}s")

        return wall_layer, block_layer, liquid_layer
