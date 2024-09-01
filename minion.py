import pygame
from game_object import GameObject
import json

with open('config.json', 'r') as file:
    config =  json.load(file)

class Minion(GameObject):
    def __init__(self, x, y, image_path, image_size, player, health, speed, damage):
        '''x, y is the bottom left corner of the image (then adjusted upwards by image height)'''
        self.player = player
        
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (image_size[0], image_size[1]))

        self.x, self.y = x, y - image_size[1]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.health = health
        self.damage = damage

        if self.player == 2:
            self.speed = -speed
            self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)

        super().__init__()

    def _move(self, delta):
        """Move the minion forwards (to the right) by its speed."""
        self.x += self.speed * delta
        self.rect.x = self.x

    def attack(self, target):
        """Attack a target if within range (e.g., collision detection)."""
        if self.rect.colliderect(target.rect):
            target.take_damage(self.damage)

    def take_damage(self, amount):
        """Reduce the minion's health by the given amount."""
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def is_destroyed(self):
        """Check if the minion is destroyed (health <= 0)."""
        return self.health <= 0
    
    def update(self, object_manager):
        self._move(object_manager.delta)

class Test(Minion):
    image_path = config['image']['minion1']
    image_size = (25, 50)
    health = 100
    speed = 100
    damage = 10

    def __init__(self, x: float, y: float, player: int):
        super().__init__(x, y, Test.image_path, Test.image_size, player, Test.health, Test.speed, Test.damage)