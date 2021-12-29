from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entity import Entity
    from gamemap import Game_Map

import pygame
import sys

class Action:
    """Generic Action class."""
    def perform(self, entity: Entity, engine: Engine)->None:
        """Perform needs to be overwritten by subclasses."""
        raise NotImplementedError()

class EscapeAction(Action):
    """Quitting the game."""
    def perform(self, entity:Entity, engine: Engine)->None:
        pygame.quit()
        sys.exit()
        raise SystemExit() #overkill?

class MovementAction(Action):
    """Generic movement action."""
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity)->None:
        try:
            dest_x = entity.x + self.dx
            dest_y = entity.y + self.dy
        except:
            pass
        if not engine.game_map.in_bounds(dest_x, dest_y):
            return
        check_tile = engine.game_map.tiles[dest_x, dest_y]
        if not check_tile.walkable:
            return
        
        try:
            engine.game_map.tiles[entity.x, entity.y].contains.remove(entity)
        except:
            pass
        entity.move(self.dx, self.dy)
        engine.game_map.tiles[entity.x, entity.y].contains.append(entity)

        
