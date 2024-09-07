import pygame
from game_object import GameObject, HealthMixin
import json
from typing import Optional

with open('config.json', 'r') as file:
    config = json.load(file)

class Minion(GameObject, HealthMixin):
    inflate_pixels = 30

    def __init__(self, x, player):
        '''x, y is the bottom left corner of the image (then adjusted upwards by image height)'''
        self.player = player
        
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, (self.image_size[0], self.image_size[1]))

        self.x, self.y = x, config['screen_height'] - config['ground_height'] - self.image_size[1]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.health = self.max_health

        if self.player == 2:
            self.speed = -self.speed
            self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)

        self.moving = True
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

    def _move(self, delta):
        """Move the minion forwards (to the right) by its speed."""
        self.x += self.speed * delta
        self.rect.x = self.x

    def detect_obstacle(self, object_manager) -> Optional[GameObject]:
        """Detect if there is an enemy or a older friendly minion in front of this minion"""
        # Iterating through list backwards to detect minions first (bases are at front of list)
        for obj in object_manager.objects[::-1]:
            parent_class_name = str(type(obj).__bases__)
            if not isinstance(obj, Minion) and not 'Base' in parent_class_name:
                continue

            if obj.collision_rect.colliderect(self.collision_rect):
                is_in_front = (self.player == 1 and obj.x > self.x) or (self.player == 2 and obj.x < self.x)
                if not is_in_front:
                    continue

                if self.player != obj.player:
                    return obj
                
                elif isinstance(obj, Minion) and obj != self:
                    return obj

        return None

    def attack(self, target):
        """Attack a target"""
        target.take_damage(self.damage)
    
    def update(self, object_manager):
        obstacle = self.detect_obstacle(object_manager)
        self.moving = obstacle is None

        # Move if nothing in the way, else try and attack if enemy
        if self.moving:
            self._move(object_manager.delta)
        elif obstacle.player != self.player:
            if self.time_to_attack < 0:
                self.attack(obstacle)
                self.time_to_attack = self.attack_interval
            else:
                self.time_to_attack -= object_manager.delta

class Test1(Minion):
    image_path = config['image']['minion1']
    image_size = (25, 50)
    max_health = 10
    speed = 100
    damage = 1
    attack_interval = 0.5
    cost = 1
    reward_xp = 1
    reward_cash = 2
    name = 'Test1'
    training_time = 2

    def __init__(self, x: float, player: int):
        super().__init__(x, player)

class Test2(Minion):
    image_path = config['image']['minion2']
    image_size = (25, 50)
    max_health = 15
    speed = 75
    damage = 2
    attack_interval = 0.7
    cost = 3
    reward_xp = 1
    reward_cash = 5
    name = 'Test2'
    training_time = 5

    def __init__(self, x: float, player: int):
        super().__init__(x, player)

class Test3(Minion):
    image_path = config['image']['minion3']
    image_size = (50, 50)
    max_health = 20
    speed = 50
    damage = 3
    attack_interval = 0.9
    cost = 6
    reward_xp = 6
    reward_cash = 9
    name = 'Test3'
    training_time = 10

    def __init__(self, x: float, player: int):
        super().__init__(x, player)