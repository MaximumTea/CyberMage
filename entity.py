import color
import gamemap
import pygame

class Entity:
    """Generic entity class to represent player, monsters, items,
        decorations, furniture, etc."""
    def __init__(
        self,
        actor_color: (int, int, int),
        start_location: (int, int),
        game_map: gamemap.Game_Map,
        iso_image: str,
        iso_offset: int,
        ):
        
        self.color = actor_color
        self.location = start_location
        x, y = self.location
        self.x = x
        self.y = y
        self.game_map = game_map
        self.game_map.tiles[x,y].contains.append(self)
        self.iso_image = pygame.image.load(iso_image)
        self.iso_image.set_colorkey(color.white)
        ## iso_offset used for images that will take more than one iso tile in height to render.
        ## for each tile height of the object, the offset should be 32 pixels.
        self.iso_offset = iso_offset
        

    def draw(self,screen,rectangle):
        """This draws a 2d representation of the entity for the minimap."""
        pygame.draw.rect(
            surface = screen,
            color = self.color,
            rect = rectangle)

    def draw_iso(self, screen, xcorn, ycorn):
        """This draws the object to the main isometric view screen."""
        newxcorn = int(xcorn)
        newycorn = int(ycorn) - int(self.iso_offset)
        screen.blit(self.iso_image, (newxcorn, newycorn))
        
    def move(self, dx: int, dy: int):
        """Moves the entity to a new location on the map."""
        x,y = self.location
        
        self.game_map.tiles[self.location].contains.remove(self)
        self.location = (x+dx, y+dy)
        self.game_map.tiles[self.location].contains.append(self)
        #this could be a problematic line
        self.game_map.player_location = self.location
        self.x, self.y = self.location


