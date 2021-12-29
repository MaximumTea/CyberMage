##CyberMage project 0.00.11 preAlpha

## image.set_alpha(0-255) makes partially transparent

##TODO:

##PRIMARY GOALS:
##CREATE A PROCEDURAL DUNGEON GENERATOR: DONE

##SECONDARY GOALS:
##ADJUST MAP GENERATION ALGORITHM SO THAT PLAYER ALWAYS RENDERS
##IN THE CENTER. DONE!
##START PLAYER IN CENTER OF FIRST ROOM   DONE!
##TILES IMMEDIATELY SURROUNDING PLAYER TO HAVE TRANSPARENCY SO THAT PLAYER
##CAN BE SEEN WHILE BEHIND TALL TILES. DEFER
##
##REMOVE PYGAME.LOAD.IMAGE FUNCTIONS FROM TILE TYPES AND ENTITY
##      SUPPORT DEEPCOPY OPERATIONS IN THE FUTURE #DONE
##DEEPCOPY TILE ARRAY SO PLAYER SHOWS UP WITHOUT HAVING TO MOVE FIRST
##  NEED TO REMOVE SCREEN ATTRIBUTES TO DEEPCOPY
##  SCREEN ATTRIBUTES REMOVES; DEEPCOPY DOES NOT WORK TO START SHOW
##  PLAYER LOCATION

import color
import dummy
from engine import Engine
from entity import Entity
from input_handlers import EventHandler
from procgen import generate_dungeon
import pygame
import sys

#initialize pygame
pygame.init()

def main():
    running = True
    screen = pygame.display.set_mode((1024,720))
    
    width, height = 80, 50 #map width and height in tiles
    view_radius = 8
    tilewidth = 10 #pixel size for two dimensional minimap tiles

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    player = Entity((color.yellow), "stickman.png", 32)

    game_map = generate_dungeon(
        max_rooms = max_rooms,
        room_min_size = room_min_size,
        room_max_size = room_max_size,
        tilewidth = tilewidth,
        map_width = width,
        map_height = height,
        viewradius = view_radius,
        player = player
        )

    entities = [player]
    event_handler = EventHandler()
    engine = Engine(
        entities = entities,
        event_handler = event_handler,
        player = player,
        game_map = game_map
        )
    engine.game_map.tiles[player.x, player.y].contains.append(player) #this line starts display of player

    while running:
        events = pygame.event.get()
        engine.handle_events(events)
        engine.render_display(screen)


if __name__ == "__main__":
    main()
