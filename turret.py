import pygame
from game_object import GameObject
import json
from typing import Optional

with open('config.json', 'r') as file:
    config =  json.load(file)

class Turret(GameObject):

    def __init__(self, x, y, player):
        self.player = player
        
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, (self.image_size[0], self.image_size[1]))
        
        self.x, self.y = x, y
        self.rect = self.image.get_rect(center=(self.x, self.y))

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

    def find_nearest_enemy(self, object_manager) -> Optional[GameObject]:
        """Detect if there is an enemy or a older friendly minion in front of this minion"""
        # # Iterating through list backwards to detect minions first (bases are at front of list)
        # for obj in object_manager.objects[::-1]:
        #     if obj.collision_rect.colliderect(self.collision_rect):
        #         is_in_front = (self.player == 1 and obj.x > self.x) or (self.player == 2 and obj.x < self.x)
        #         if not is_in_front:
        #             continue

        #         if self.player != obj.player:
        #             return obj
                
        #         elif isinstance(obj, Minion) and obj != self:
        #             return obj

        return None

    def shoot(self, target):
        ...
    
    def update(self, object_manager):
        nearest_enemy = self.find_nearest_enemy(object_manager)
        if nearest_enemy is None:
            return
        # self.moving = obstacle is None

        # # Move if nothing in the way, else try and attack if enemy
        # if self.moving:
        #     self._move(object_manager.delta)
        # elif obstacle.player != self.player:
        #     if self.time_to_attack < 0:
        #         self.attack(obstacle)
        #         self.time_to_attack = self.attack_interval
        #     else:
        #         self.time_to_attack -= object_manager.delta

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