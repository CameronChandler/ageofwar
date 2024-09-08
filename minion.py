import pygame
from game_object import GameObject, HealthMixin
import json
from typing import Optional
from constants import CONFIG_NAME

with open(CONFIG_NAME, 'r') as file:
    config = json.load(file)

class Minion(GameObject, HealthMixin):
    inflate_pixels = 30
    speed = 150

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

    @classmethod
    def load_attributes_from_config(cls):
        """Load static attributes for a specific minion type from the config."""
        cls.image_path = config['image'][cls.minion_id]
        cls.max_health = config['minion_stats'][cls.minion_id]['max_health']
        cls.damage     = config['minion_stats'][cls.minion_id]['damage']
        cls.cost       = config['minion_stats'][cls.minion_id]['cost']
        cls.reward_xp  = config['minion_stats'][cls.minion_id]['reward_xp']

class Chimp(Minion):
    minion_id = 'minion1'
    image_size = (25, 50)
    attack_interval = 0.5
    reward_cash = 2
    training_time = 0.5

    def __init__(self, x: float, player: int):
        super().__init__(x, player)

class Clubman(Minion):
    minion_id = 'minion2'
    image_size = (25, 50)
    max_health = 15
    attack_interval = 0.7
    reward_cash = 5
    training_time = 0.8

    def __init__(self, x: float, player: int):
        super().__init__(x, player)

class Dino(Minion):
    minion_id = 'minion3'
    image_size = (50, 50)
    max_health = 20
    attack_interval = 0.9
    reward_cash = 9
    training_time = 1.5

    def __init__(self, x: float, player: int):
        super().__init__(x, player)

class Jester(Minion):
    minion_id = 'minion4'
    image_size = (25, 50)
    max_health = 30
    attack_interval = 0.5
    reward_cash = 15
    training_time = 1.5

    def __init__(self, x: float, player: int):
        super().__init__(x, player)

class Knight(Minion):
    minion_id = 'minion5'
    image_size = (25, 50)
    max_health = 50
    attack_interval = 0.7
    reward_cash = 25
    training_time = 2

    def __init__(self, x: float, player: int):
        super().__init__(x, player)

class Horse(Minion):
    minion_id = 'minion6'
    image_size = (25, 50)
    max_health = 80
    attack_interval = 0.9
    reward_cash = 50
    training_time = 2.5

    def __init__(self, x: float, player: int):
        super().__init__(x, player)

class Soldier(Minion):
    minion_id = 'minion7'
    image_size = (25, 50)
    max_health = 120
    attack_interval = 0.4
    reward_cash = 80
    training_time = 2.5

    def __init__(self, x: float, player: int):
        super().__init__(x, player)

class Rambo(Minion):
    minion_id = 'minion8'
    image_size = (25, 50)
    max_health = 150
    attack_interval = 0.6
    reward_cash = 120
    training_time = 3

    def __init__(self, x: float, player: int):
        super().__init__(x, player)

class Tank(Minion):
    minion_id = 'minion9'
    image_size = (25, 50)
    max_health = 250
    attack_interval = 1.0
    reward_cash = 180
    training_time = 3.5

    def __init__(self, x: float, player: int):
        super().__init__(x, player)

class Alien(Minion):
    minion_id = 'minion10'
    image_size = (25, 50)
    max_health = 300
    attack_interval = 0.4
    reward_cash = 250
    training_time = 3.5

    def __init__(self, x: float, player: int):
        super().__init__(x, player)

class Robot(Minion):
    minion_id = 'minion11'
    image_size = (25, 50)
    max_health = 500
    attack_interval = 0.2
    reward_cash = 350
    training_time = 4

    def __init__(self, x: float, player: int):
        super().__init__(x, player)

class UFO(Minion):
    minion_id = 'minion12'
    image_size = (25, 50)
    max_health = 1000
    attack_interval = 0.1
    reward_cash = 500
    training_time = 5

    def __init__(self, x: float, player: int):
        super().__init__(x, player)

for cls in (Chimp, Clubman, Dino, Jester, Knight, Horse, Soldier, Rambo, Tank, Alien, Robot, UFO):
    cls.load_attributes_from_config()

MINION_CHOICES = {
    0: {'spawn_1': Chimp,   'spawn_2': Clubman, 'spawn_3': Dino},
    1: {'spawn_1': Jester,  'spawn_2': Knight,  'spawn_3': Horse},
    2: {'spawn_1': Soldier, 'spawn_2': Rambo,   'spawn_3': Tank},
    3: {'spawn_1': Alien,   'spawn_2': Robot,   'spawn_3': UFO},
}