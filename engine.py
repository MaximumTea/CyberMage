#Engine class

from __future__ import annotations


import color
from entity import Entity
from gamemap import Game_Map
from input_handlers import EventHandler
import numpy as np
import pygame
from typing import Set


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
        self.game_map = game_map

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
        for x in (self.tiles):
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


    def view_bounds(self, x_start, y_start, view_x, view_y):
        """ This function returns the values for tile placement for the player
            centered maps. It currently does not work in small map areas, and
            seems a little janky, but it works for now."""
        
        origin_x, origin_y = self.game_map.player_location

        #test x bounds alternative algorithm:

        if origin_x < view_x:
            if origin_x + view_x > self.game_map.mapwidth:
                xmin = 0
                xmax = self.game_map.mapwidth
            else:
                xmin = 0
                xmax = view_x
        else:
            xmin = origin_x - view_x

        if origin_x + view_x > self.game_map.mapwidth:
            xmin = self.game_map.mapwidth - 2*view_x
            xmax = self.game_map.mapwidth

        else:
            xmax = origin_x + view_x

##        #test x lower bounds:
##        if origin_x < view_x:
##            xmin = 0
##            xmax = view_x
##
##        else:
##            xmin = origin_x - view_x
##
##        #test the x upper bounds
##        if origin_x + view_x > self.game_map.mapwidth:
##            xmin = self.game_map.mapwidth - 2*view_x
##            xmax = self.game_map.mapwidth
##        else:
##            xmax = origin_x + view_x

        #test the y lower bounds
        if origin_y < view_y:
            ymin = 0
            ymax = view_y
        else:
            ymin = origin_y - view_y

        #test the y upper bounds
        if origin_y + view_y > self.game_map.mapheight:
            ymin = self.game_map.mapheight - 2*view_y
            ymax = self.game_map.mapheight
        else:
            ymax = origin_y + view_y

        return (xmin, xmax, ymin, ymax)

    def render_2d_playercenter(self, surface, x_start, y_start, view_x, view_y):
        """Create 2d map of section in the view radius of the player."""
        xstep = -self.game_map.tilewidth
        ystep = 0

        xmin, xmax, ymin, ymax = self.view_bounds(x_start -32, y_start, view_x, view_y)
        tilescopy = np.copy(self.game_map.tiles) #make copy of original tileset to ensure that the original is preserved
        tileset = tilescopy[xmin:xmax, ymin:ymax]
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

    def render_iso(self, surface, x_start, y_start, view_x, view_y):
        """Renders the isometric view of the map and entities."""

        xmin, xmax, ymin, ymax = self.view_bounds(x_start, y_start, view_x, view_y)
        tilescopy = np.copy(self.game_map.tiles) #make copy of original tileset to ensure that the original is preserved
        tileset = tilescopy[xmin:xmax, ymin:ymax]
        xstep = -1
        for x in (tileset):
            ystep = -1
            xstep += 1
            for y in x:
                ystep += 1
                xcorn = x_start + xstep * 32 - ystep * 32
                ycorn = y_start + xstep * 16 + ystep * 16
                surface.blit(y.iso_image, ((xcorn), (ycorn + y.iso_offset)))
                if y.contains is not []:
                    for contained_object in y.contains:
                        contained_object.draw_iso(surface, xcorn, ycorn)
        

    def rotate_surface(self, surface):
        """Rotate surface to approximately a game iso angle."""
        return pygame.transform.rotate(surface, -63)
#        return pygame.transform.rotate(surface, -45)
        

    def render_display(self, screen):
        """This will be the function responsible for the overall graphics display of the map."""
        screen.fill(color.white)
        self.render_2d_playercenter(
            self.game_map.gridsurface, 10, 10,
            self.game_map.view_x, self.game_map.view_y)
        new_surface = self.rotate_surface(self.game_map.gridsurface)
        new_surface.set_colorkey(color.white)
        xoffset = int(-7.3 * self.game_map.view_x)
        self.render_iso(screen, int(screen.get_width() / 2), 128 , self.game_map.view_x, self.game_map.view_y)
        screen.blit(new_surface, (xoffset, 0))
        pygame.display.flip()


