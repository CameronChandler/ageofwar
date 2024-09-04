import pygame
from game_object import GameObject, HealthBarMixin
import json

with open('config.json', 'r') as file:
    config =  json.load(file)

class Minion(GameObject, HealthBarMixin):
    inflate_pixels = 30

    def __init__(self, x, image_path, image_size, player, health, speed, damage):
        '''x, y is the bottom left corner of the image (then adjusted upwards by image height)'''
        self.player = player
        
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (image_size[0], image_size[1]))

        self.x, self.y = x, config['screen_height'] - config['ground_height'] - image_size[1]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.max_health = self.health = health
        self.damage = damage

        if self.player == 2:
            self.speed = -speed
            self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)

        self.moving = True
        self.obstacle = None

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

    def _move(self, delta):
        """Move the minion forwards (to the right) by its speed."""
        self.x += self.speed * delta
        self.rect.x = self.x

    def detect_obstacle(self, object_manager):
        """Detect if there is an enemy or a older friendly minion in front of this minion"""
        # Iterating through list backwards to detect minions first (bases are at front of list)
        for obj in object_manager.objects[::-1]:
            if obj.collision_rect.colliderect(self.collision_rect):
                if self.player != obj.player:
                    self.obstacle = obj
                    return True
                
                elif isinstance(obj, Minion) and obj != self:
                    self.obstacle = obj
                    return True

        self.obstacle = None
        return False

    # def attack(self, target):
    #     """Attack a target if within range (e.g., collision detection)."""
    #     if self.rect.colliderect(target.rect):
    #         target.take_damage(self.damage)

    # def take_damage(self, amount):
    #     """Reduce the minion's health by the given amount."""
    #     self.health -= amount
    #     if self.health < 0:
    #         self.health = 0

    # def is_destroyed(self):
    #     """Check if the minion is destroyed (health <= 0)."""
    #     return self.health <= 0
    
    def update(self, object_manager):
        self.moving = not self.detect_obstacle(object_manager)

        if self.moving:
            self._move(object_manager.delta)

class Test1(Minion):
    image_path = config['image']['minion1']
    image_size = (25, 50)
    health = 100
    speed = 100
    damage = 10
    cost = 1
    name = 'Test1'
    training_time = 2

    def __init__(self, x: float, player: int):
        super().__init__(x, Test1.image_path, Test1.image_size, player, Test1.health, Test1.speed, Test1.damage)

class Test2(Minion):
    image_path = config['image']['minion2']
    image_size = (25, 50)
    health = 100
    speed = 100
    damage = 10
    cost = 1
    name = 'Test2'
    training_time = 2

    def __init__(self, x: float, player: int):
        super().__init__(x, Test2.image_path, Test2.image_size, player, Test2.health, Test2.speed, Test2.damage)

class Test3(Minion):
    image_path = config['image']['minion3']
    image_size = (50, 50)
    health = 100
    speed = 100
    damage = 10
    cost = 1
    name = 'Test3'
    training_time = 2

    def __init__(self, x: float, player: int):
        super().__init__(x, Test3.image_path, Test3.image_size, player, Test3.health, Test3.speed, Test3.damage)