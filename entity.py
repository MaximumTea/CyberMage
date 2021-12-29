import color
# import gamemap
import pygame

class Entity:
    """Generic entity class to represent player, monsters, items,
        decorations, furniture, etc."""
    def __init__(
        self,
        actor_color: (int, int, int),
        iso_image: str,
        iso_offset: int,
        ):
        
        self.color = actor_color
        self.location = (0,0)
        x,y = self.location
        self.x = x
        self.y = y

        self.iso_image = iso_image
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
        image = pygame.image.load(self.iso_image)
        image.set_colorkey(color.white)
        screen.blit(image, (newxcorn, newycorn))
        
    def move(self, dx: int, dy: int):
        """Moves the entity to a new location on the map."""
        x,y = self.location

        self.location = (x+dx, y+dy)
        self.x, self.y = self.location


