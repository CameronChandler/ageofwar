import pygame
from constants import Color

class GameObject:
    inflate_pixels = 10

    def __init__(self):
        self.to_draw = True
        self.zorder = 0
        self.age = pygame.time.get_ticks()

    @property
    def collision_rect(self):
        """Return an inflated rectangle centered around the original rectangle."""
        return self.rect.inflate(self.inflate_pixels, 0)


    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, object_manager):
        ...

    def draw_collision_rect(self, screen):
        """Draw the collision rectangle for debugging purposes."""
         # Red rectangle with a 2-pixel border
        pygame.draw.rect(screen, Color.RED, self.collision_rect, 2)
