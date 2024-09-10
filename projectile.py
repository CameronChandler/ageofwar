import pygame
from game_object import GameObject
import json
from math import radians, cos, sin
from constants import CONFIG_NAME

with open(CONFIG_NAME, 'r') as file:
    config = json.load(file)

class Projectile(GameObject):
    def __init__(self, x, y, angle, player):
        self.x, self.y, self.angle, self.player = x, y, angle, player

        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, (self.image_size[0], self.image_size[1]))
        self.image = pygame.transform.rotate(self.image, -self.angle)

        self.rect = self.image.get_rect(center=(self.x, self.y))

        super().__init__()

    def move(self, delta):
        """Move the projectile in the direction of its angle."""
        rad_angle = radians(self.angle)  # Convert the angle to radians
        # Update the position based on the angle and speed
        self.x += self.speed * cos(rad_angle) * delta
        self.y += self.speed * sin(rad_angle) * delta
        self.rect.center = (self.x, self.y)  # Update the rect's position

    def update(self, object_manager):
        """Update the projectile position and check for collisions."""
        # Move the projectile
        self.move(object_manager.delta)

        # Check if the projectile hits an enemy
        for obj in object_manager.objects:
            parent_class_name = str(type(obj).__bases__)
            if not 'Minion' in parent_class_name and not 'Base' in parent_class_name:
                continue

            if obj.player != self.player and self.rect.colliderect(obj.rect):
                self.on_hit(obj)
                object_manager.remove_object(self)
                break

    def on_hit(self, target):
        """Handle what happens when the projectile hits a target."""
        target.health -= self.damage

class Egg(Projectile):
    image_path = config['image']['projectile1']
    image_size = (7, 10)
    speed = 200
    damage = 10

    def __init__(self, x: float, y: float, angle: float, player: int):
        super().__init__(x, y, angle, player)

class Arrow(Projectile):
    image_path = config['image']['projectile2']
    image_size = (8, 2)
    speed = 400
    damage = 10

    def __init__(self, x: float, y: float, angle: float, player: int):
        super().__init__(x, y, angle, player)

class Bullet(Projectile):
    image_path = config['image']['projectile3']
    image_size = (6, 2)
    speed = 600
    damage = 10

    def __init__(self, x: float, y: float, angle: float, player: int):
        super().__init__(x, y, angle, player)

class Laser(Projectile):
    image_path = config['image']['projectile4']
    image_size = (10, 3)
    speed = 1000
    damage = 10

    def __init__(self, x: float, y: float, angle: float, player: int):
        super().__init__(x, y, angle, player)