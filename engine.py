#Engine class

from __future__ import annotations


import color
from entity import Entity
from gamemap import Game_Map
from input_handlers import EventHandler
import numpy as np
import pygame
from typing import Set
import copy


##ADDING FULL_MAP REFERENCES TO RENDER FUNCTIONS

##MAKE GRIDSURFACE AN ENGINE ATTRIBUTE

class Engine:
    """The engine class is responsible for handling event handlers and rendering
    the game map and game objects."""
    def __init__(
        self,
        entities: Set[Entity],
        event_handler: EventHandler,
        player: Entity,
        game_map: Game_Map
        ):
        self.entities = entities
        self.event_handler = event_handler
        self.player = player
#        self.game_map = copy.deepcopy(game_map) #Does not work as intended
        self.game_map = game_map
        xstep = -1
        
        self.gridsurface = pygame.Surface((300,300))
        self.gridsurface.fill(color.white)

    def handle_events(self, events) -> None:
        """Refer events to the event handler and perform appropriate action."""
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)

###RENDERING FUNCTIONS:
###Render non-player centered full map area

    def render_2d(self, surface, x_start, y_start):
        """Create a 2D map of entire map to be pasted onto a surface object.
        Not currently used, but will be used later as a way to draw a full
        map that the player can access."""
        xstep = -self.game_map.tilewidth
        ystep = 0
        for x in (self.full_tiles):
            ystep = -self.game_map.tilewidth
            xstep += self.game_map.tilewidth
            for y in x:
                ystep += self.game_map.tilewidth
                salsa = pygame.Rect(
                    ((x_start + xstep),
                    (y_start + ystep)),
                    (self.game_map.tilewidth - 1,
                    self.game_map.tilewidth - 1)
                    )
                pygame.draw.rect(
                    surface = surface,
                    color = y.color_seen,
                    rect = salsa
                    )
                if y.contains is not []:
                    for contained_object in y.contains:
                        contained_object.draw(surface, salsa)


    def view_bounds(self, x_start, y_start, viewradius):
        """ This function returns the values for tile placement for the player
            centered maps. It currently does not work in small map areas, and
            seems a little janky, but it works for now."""
        
        origin_x, origin_y = self.player.location
        origin_x += viewradius
        origin_y += viewradius
        #test x bounds

        if origin_x < viewradius:
            if origin_x + viewradius > self.game_map.fullwidth:
                xmin = 0
                xmax = self.game_map.fullwidth
            else:
                xmin = 0
                xmax = viewradius
        else:
            xmin = origin_x - viewradius


        if origin_x + viewradius > self.game_map.fullwidth:
            xmin = self.game_map.fullwidth - 2*viewradius
            xmax = self.game_map.fullwidth

        else:
            xmax = origin_x + viewradius

        #test the y lower bounds
        if origin_y < viewradius:
            ymin = 0
            ymax = viewradius
        else:
            ymin = origin_y - viewradius

        if origin_y + viewradius > self.game_map.fullheight:
            ymin = self.game_map.fullheight - 2*viewradius
            ymax = self.game_map.fullheight
        else:
            ymax = origin_y + viewradius

        return (xmin, xmax, ymin, ymax)

    def transparent_bounds(self, x_start, y_start, transparency_radius):
        """This function determines which tile areas should apply a transparent filter.
        This makes sure that the player can see through appropriate walls to be able to
        make out important game details."""

    def render_2d_playercenter(self, surface, x_start, y_start, viewradius):
        """Create 2d map of section in the view radius of the player."""
        xstep = -self.game_map.tilewidth
        ystep = 0

        xmin, xmax, ymin, ymax = self.view_bounds(x_start -32, y_start, viewradius)
        tileset = self.game_map.full_tiles[xmin:xmax, ymin:ymax]
        for x in (tileset):
            ystep = -self.game_map.tilewidth
            xstep += self.game_map.tilewidth
            for y in x:
                ystep += self.game_map.tilewidth
                salsa = pygame.Rect(
                    ((x_start + xstep),
                    (y_start + ystep)),
                    (self.game_map.tilewidth - 1,
                    self.game_map.tilewidth - 1)
                    )
                pygame.draw.rect(
                    surface = surface,
                    color = y.color_seen,
                    rect = salsa
                    )
                if y.contains is not []:
                    for contained_object in y.contains:
                        contained_object.draw(surface, salsa)

    def render_iso(self, surface, x_start, y_start, viewradius):
        """Renders the isometric view of the map and entities."""
        ###IN PROGRESS: CHANGING THIS FUNCTION TO WORK WITHOUT DIRECT IMAGE LOAD FROM TILES

        #TEMPORARY DICT STRUCTURE TO IMPROVE PERFORMACE:
        image_dict = {
            "floor" : pygame.image.load("iso64x32base4_grass.png"),
            "wall" : pygame.image.load("iso64x32base4depth3.png"),
            "void" : pygame.image.load("empty.png")
            }



        xmin, xmax, ymin, ymax = self.view_bounds(x_start, y_start, viewradius)
        tileset = self.game_map.full_tiles[xmin:xmax, ymin:ymax]
        xstep = -1
        for x in (tileset):
            ystep = -1
            xstep += 1
            for y in x:
                ystep += 1
                xcorn = x_start + xstep * 32 - ystep * 32
                ycorn = y_start + xstep * 16 + ystep * 16
                image = image_dict[y.name]
                offset = y.iso_offset

                # creating transparent zone #
#                if y.name == "wall" and ystep > self.player.y:
#                if y.name == "wall" and (ystep > viewradius or xstep > viewradius):
#                    image = image_dict["void"]
#                    offset = 0
#                if y.name == "wall" and xstep > self.player.x:
#                if y.name == "wall" and xstep > viewradius:
#                    image = image_dict["void"]
#                    offset = 0
                ##############################
                image.set_colorkey(color.white)
                surface.blit(image, ((xcorn), (ycorn + offset)))
                if y.contains is not []:
                    for contained_object in y.contains:
                        contained_object.draw_iso(surface, xcorn, ycorn)
        

    def rotate_surface(self, surface):
        """Rotate surface to approximately a game iso angle."""
        return pygame.transform.rotate(surface, -63)
        

    def render_display(self, screen):
        """This will be the function responsible for the overall graphics display of the map."""
        screen.fill(color.white)
        self.render_2d_playercenter(
            self.gridsurface, 10, 10,
            self.game_map.viewradius)
        new_surface = self.rotate_surface(self.gridsurface)
        new_surface.set_colorkey(color.white)
        xoffset = int(-7.3 * self.game_map.viewradius)
        self.render_iso(screen, int(screen.get_width() / 2), 128 , self.game_map.viewradius)
        screen.blit(new_surface, (xoffset, 0))
        pygame.display.flip()


