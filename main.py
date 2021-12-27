##CyberMage project 0.00.10 preAlpha


##TODO:
## SPLITTING MODULES: DONE
    ##BULK CLASS TRANSFER: DONE
    ##DEPENDENCY UPDATES: DONE
    ##CLASS LOGIC UPDATES: DONE
## CODE CLEANUP:
    ##COMBINE GENERIC X,Y ARGUMENTS AS TUPLE ARGUMENTS - DEFER
    ##ADD ANNOTATIONS TO CLASSES AND FUNCTIONS: CONTINUOUS PROGRESS
    ##ADD VERSION NUMBER TO MAIN: DONE
    ##Simplify: tile width & tile height to one variable: square tiles: DONE
## UPLOAD TO GITHUB: CONTINUOUS PROGRESS
## RENAME ACTOR TO ENTITY: DONE
## EVALUATE CIRCULAR IMPORTS: DONE [but I don't understand how it works]
##      -REMOVE ENGINE IMPORT FROM ACTIONS? NO, ADDED TYPECHECKING ARGS
##      -BIG JUJU DONE
## MOVE PYGAME FLIP TO ENGINE RENDERING FUNCTION: DONE
## IN ENGINE RENDER FUNCTIONS, CREATE A FUNCTION TO SIMPLIFY VISUAL BOUNDARY CHECKS: DONE

import color
import dummy
from engine import Engine
from entity import Entity
from input_handlers import EventHandler
from gamemap import Game_Map
import pygame
import sys

#initialize pygame
pygame.init()

def main():
    running = True
    screen = pygame.display.set_mode((900,600))
    
    width, height = 80, 50 #map width and height in tiles
    view_radius = 7
    tilewidth = 10 #pixel size for two dimensional minimap tiles

    player_start = (10,10) #player start location in x, y tiles
    game_map = Game_Map(
        tilewidth = tilewidth,
        width = width,
        height = height,
        view_x = view_radius,
        view_y = view_radius,
        screen = screen,
        player_start = player_start
        )
    player = Entity((color.red), player_start, game_map, "stickman.png", 32)

    entities = [player]
    event_handler = EventHandler()
    engine = Engine(
        entities = entities,
        event_handler = event_handler,
        player = player,
        game_map = game_map
        )

    while running:
        events = pygame.event.get()
        engine.handle_events(events)
        engine.render_display(screen)


if __name__ == "__main__":
    main()
