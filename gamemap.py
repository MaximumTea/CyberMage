import color
from dummy import dummy, DummyObject
import numpy as np
from tile_types import *

class Game_Map:
    def __init__(self, tilewidth: int, width: int, height: int, view_x: int, view_y: int, screen, player_start):
        self.tilewidth = tilewidth
        self.mapwidth = width
        self.mapheight = height
        self.view_x = view_x
        self.view_y = view_y
        self.tiles = np.full((width,height), dummy, order = "F")
        self.gen_map_array()

        
        self.tiles[0:5, 1] = new_tile("wall")  #change some tiles to a dummy wall to test the new player centric map function
        
        self.screen = screen
        self.gridsurface = pygame.Surface((300,300))
        self.gridsurface.fill(color.white)
        self.player_location = player_start

        self.change_tiles(20, 30, 10, 10, "wall")


    def change_tiles(self, x_start, y_start, x_change: int, y_change: int, tile_type: str):
        xrange = x_start + x_change
        yrange = y_start + y_change
        tilechunk = self.tiles[x_start:xrange , y_start:yrange]
        tilescopy = np.copy(tilechunk) #make copy of original tileset to ensure that the original is preserved
        xincr = -1
        for x in tilechunk:
            xincr += 1
            yincr = -1

            for y in x:
                yincr += 1
                tilechunk[xincr, yincr] = new_tile(tile_type)

        self.tiles[x_start:xrange, y_start:yrange] = tilechunk
            
        
        
####new function to generate an array of individual tiles of the new type.
    def gen_map_array(self):
        """Fill the map array with tiles"""
        xincr = -1
        yincr = -1
        for x in (self.tiles):
            xincr += 1
            yincr = -1
            
            for y in x:

                yincr += 1
                change_tile = new_tile("floor")
                self.tiles[xincr,yincr] = change_tile
        

    def in_bounds(self, x:int, y:int) -> bool:
        """Check to see if object is inside the map bounds."""
        return 0 <= x < self.mapwidth and 0 <= y < self.mapheight


    def check_walkable(self, x: int, y:int) -> bool:
        """Check to see if tile is walkable."""
        tile = game_map.tiles[x,y]
        return tile.walkable
