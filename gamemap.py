import color
from dummy import dummy, DummyObject
import numpy as np
from tile_types import *


class Game_Map:
    def __init__(self, tilewidth: int, width: int, height: int, viewradius: int):
        self.tilewidth = tilewidth
        self.mapwidth = width
        self.mapheight = height
        self.viewradius = viewradius
        self.fullwidth = width + viewradius
        self.fullheight = height + viewradius
        self.full_tiles = np.full((width + viewradius,height + viewradius), dummy, order = "F") #fill map with void tiles
        self.tiles = self.full_tiles[viewradius : viewradius + width, viewradius : viewradius + height] #define play map cutout of full map
        self.gen_map_array()
        


    def change_tiles(self, area, tile_type:str):
        tilechunk = self.tiles[area]
        xincr = -1
        for x in tilechunk:
            xincr += 1
            yincr = -1

            for y in x:
                yincr += 1
                tilechunk[xincr, yincr] = new_tile(tile_type)

    def change_single_tile(self, tile: (int, int), tile_type:str):
        self.tiles[tile] = new_tile(tile_type)
        
        
####new function to generate an array of individual tiles of the new type.
    def gen_map_array(self):
        """Fill the map array with void tiles and then
        wall fill on top of the playable area of the map."""
        xincr = -1
        for x in (self.full_tiles):
            xincr += 1
            yincr = -1
            
            for y in x:

                yincr += 1
                tile_fill = new_tile("void")
                self.full_tiles[xincr,yincr] = tile_fill

        tilechunk = self.tiles
        xincr = -1
        for x in tilechunk:
            xincr += 1
            yincr = -1
            for y in x:
                yincr += 1
                tile_fill = new_tile("wall")
                self.tiles[xincr,yincr] = tile_fill

        
        

    def in_bounds(self, x:int, y:int) -> bool:
        """Check to see if object is inside the map bounds."""
        return 0 <= x < self.mapwidth and 0 <= y < self.mapheight


    def check_walkable(self, x: int, y:int) -> bool:
        """Check to see if tile is walkable."""
        tile = game_map.tiles[x,y]
        return tile.walkable
