import pygame
from game_object import GameObject
import json
from typing import Optional
from math import atan2, degrees

with open('config.json', 'r') as file:
    config = json.load(file)

class Turret(GameObject):

    def __init__(self, x, y, player):
        self.player = player
        
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, (self.image_size[0], self.image_size[1]))
        self.original_image = self.image.copy()
        
        self.x, self.y = x, y
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        
        self.angle = 0
        if self.player == 2:
            self.speed = -self.speed
            self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)

        self.time_to_attack = self.attack_interval

        super().__init__()

    @property
    def name():
        raise NotImplementedError

    @property
    def cost():
        raise NotImplementedError

    @property
    def training_time():
        raise NotImplementedError

    @property
    def attack_interval():
        raise NotImplementedError
    
    def distance(self, obj1, obj2):
        return ((obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2) ** 0.5

    def find_nearest_enemy(self, object_manager) -> Optional[GameObject]:
        """Find the nearest enemy within a certain range."""
        nearest_enemy = None
        nearest_distance = float('inf')

        for obj in object_manager.objects:
            if obj.player != self.player:
                distance = self.distance(self, obj)
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_enemy = obj

        return nearest_enemy

    def shoot(self, target):
        ...

    def rotate_toward(self, target):
        """Rotate the turret to point at the target."""
        # Calculate the angle to the target in radians
        dx = target.center_x - self.center_x
        dy = target.center_y - self.center_y
        self.angle = degrees(atan2(dy, dx))  # Convert to degrees

        # Rotate the image to point at the target
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=(self.center_x, self.center_y))
    
    def update(self, object_manager):
        nearest_enemy = self.find_nearest_enemy(object_manager)
        if nearest_enemy is None:
            return

        # Rotate to face the nearest enemy
        self.rotate_toward(nearest_enemy)

        # Check if it's time to attack
        if self.time_to_attack <= 0:
            self.shoot(nearest_enemy)
            self.time_to_attack = self.attack_interval  # Reset attack timer
        else:
            self.time_to_attack -= object_manager.delta  # Countdown timer

class Turret1(Turret):
    image_path = config['image']['turret1']
    image_size = (60, 10)
    max_health = 100
    speed = 100
    damage = 10
    attack_interval = 0.5
    cost = 1
    reward_xp = 1
    reward_cash = 1
    name = 'Turret1'
    training_time = 2

    def __init__(self, x: float, y: float, player: int):
        super().__init__(x, y, player)