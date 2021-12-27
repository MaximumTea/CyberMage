import color
import pygame

#Tile construction

class Tile:
    def __init__(
        self,
        walkable: bool,
        transparent: bool,
        color_notseen: (int, int, int),
        color_seen: (int,int,int),
        color_fade: (int,int,int),
        contains: [],
        iso_image: str,
        iso_offset: int
        ):

        self.walkable = walkable
        self.transparent = transparent
        self.color_notseen = color_notseen
        self.color_seen = color_seen
        self.color_fade = color_fade
        self.contains = []
        self.iso_image = pygame.image.load(iso_image)
        self.iso_image.set_colorkey(color.white)
        self.iso_offset = iso_offset

#Create a basic floor and wall tile type

def new_tile(tile_type):
    if tile_type == "floor":
        tile = Tile(
            walkable = True,
            transparent = True,
            color_notseen = color.black,
            color_seen = color.light_grey,
            color_fade = (128,128,200),
            contains = [],
            iso_image = "iso64x32base4_grass.png",
            iso_offset = 0
            )
        return tile
    elif tile_type == "wall":
        tile = Tile(
            walkable = False,
            transparent = False,
            color_notseen = color.black,
            color_seen = color.grey,
            color_fade = (200,200,255),
            contains = [],
            iso_image = "iso64x32base4depth3.png",
            iso_offset = -96
            )
        return tile
