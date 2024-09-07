import pygame
from constants import Color

class GameObject:
    inflate_pixels = 10

    def __init__(self):
        self.to_draw = True
        self.zorder = 0
        self.age = pygame.time.get_ticks()

    @property
    def center_x(self):
        return self.x + self.image_size[0]/2

    @property
    def center_y(self):
        return self.y + self.image_size[1]/2
    
    @property
    def collision_rect(self):
        """Return an inflated rectangle centered around the original rectangle."""
        return self.rect.inflate(self.inflate_pixels, 0)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, object_manager):
        raise NotImplementedError

    def draw_collision_rect(self, screen):
        """Draw the collision rectangle for debugging purposes."""
         # Red rectangle with a 2-pixel border
        pygame.draw.rect(screen, Color.RED, self.collision_rect, 2)

class HealthMixin:

    def __init__(self):
        self.max_health = self.health = None

    def draw_health_bar(self, screen):
        """Draw the health bar above the object."""
        bar_width = self.rect.width
        bar_height = 5
        health_ratio = self.health / self.max_health
        green_width = int(bar_width * health_ratio)

        bar_x = self.x
        bar_y = self.y - 10  # 10 pixels above the object

        pygame.draw.rect(screen, Color.RED  , (bar_x, bar_y,   bar_width, bar_height))
        pygame.draw.rect(screen, Color.GREEN, (bar_x, bar_y, green_width, bar_height))

    def take_damage(self, damage):
        """Reduce the minion's health by the given damage"""
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def is_destroyed(self):
        """Check if the minion is destroyed (health <= 0)."""
        return self.health <= 0