from __future__ import annotations
from gamemap import Game_Map
import tile_types
import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entity import Entity


class RectangularRoom:
    def __init__(self, x:int, y:int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height


    @property
    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        center = [center_x, center_y]

        return  center

    @property
    def inner(self):
        """Return the inner area of this room as a 2D array index."""
        return (slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2))

    def intersects(self, other: RectangularRoom) -> bool:
        """Returns True if this room overlaps with another Rectangular Room."""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
            )

def tunnel_between(
    start: (int, int),
    end: (int, int)
    ):


    x1, y1 = start
    x2, y2 = end
    
    if random.random() < 0.5:
        #Move horizontally then vertically
        corner_x, corner_y = x2, y1
    else:
        #Move vertically then horizontally
        corner_x, corner_y = x1, y2

    chunk1 = sorted((x1, corner_x))
    slicepiece1 = slice(chunk1[0], chunk1[1] + 1)
    chunk2 = sorted((y1, corner_y))
    slicepiece2 = slice(chunk2[0], chunk2[1] + 1)
    chunk3 = sorted((corner_x, x2))
    slicepiece3 = slice(chunk3[0], chunk3[1] + 1)
    chunk4 = sorted((corner_y, y2))
    slicepiece4 = slice(chunk4[0], chunk4[1] + 1)

    area1 = (slicepiece1, slicepiece2)
    area2 = (slicepiece3, slicepiece4)

    cut = [area1, area2]
    return cut



def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    tilewidth,
    map_width,
    map_height,
    viewradius,
    player: Entity,
    ) -> Game_Map:

    
    dungeon = Game_Map(
        tilewidth,
        map_width,
        map_height,
        viewradius,
        )

    rooms = [] #list of rooms

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.mapwidth - room_width - 1)
        y = random.randint(0, dungeon.mapheight - room_height - 1)

        new_room = RectangularRoom(x, y, room_width, room_height)

        if any(new_room.intersects(other_room) for other_room in rooms):
            continue #Room instersects, so it doesn't get placed.

        dungeon.change_tiles(new_room.inner, "floor")

        if len(rooms) == 0: #room where player first starts
            xloc, yloc = new_room.center
            player.location = (xloc, yloc)
            player.x = xloc
            player.y = yloc
            

        else:
            #dig tunnel
            for area in tunnel_between(rooms[-1].center, new_room.center):                    
                dungeon.change_tiles(area, "floor")

        rooms.append(new_room)
    return dungeon
