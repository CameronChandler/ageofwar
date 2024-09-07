import pygame
from game_object import GameObject, HealthMixin
import json
from typing import Optional
from constants import CONFIG_NAME

with open(CONFIG_NAME, 'r') as file:
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

class Chimp(Minion):
    image_path = config['image']['minion1']
    image_size = (25, 50)
    max_health = 10
    speed = 75
    damage = 1
    attack_interval = 0.5
    cost = 1
    reward_xp = 1
    reward_cash = 2
    name = 'Chimp'
    training_time = 0.5

    def __init__(self, x: float, player: int):
        super().__init__(x, player)

class ClubMan(Minion):
    image_path = config['image']['minion2']
    image_size = (25, 50)
    max_health = 15
    speed = 75
    damage = 2
    attack_interval = 0.7
    cost = 3
    reward_xp = 3
    reward_cash = 5
    name = 'Clubman'
    training_time = 0.8

    def __init__(self, x: float, player: int):
        super().__init__(x, player)

class Dino(Minion):
    image_path = config['image']['minion3']
    image_size = (50, 50)
    max_health = 20
    speed = 75
    damage = 3
    attack_interval = 0.9
    cost = 6
    reward_xp = 6
    reward_cash = 9
    name = 'Dino'
    training_time = 1.5

    def __init__(self, x: float, player: int):
        super().__init__(x, player)

class Jester(Minion):
    image_path = config['image']['minion4']
    image_size = (25, 50)
    max_health = 30
    speed = 75
    damage = 4
    attack_interval = 0.5
    cost = 10
    reward_xp = 15
    reward_cash = 15
    name = 'Jester'
    training_time = 1.5

    def __init__(self, x: float, player: int):
        super().__init__(x, player)

class Knight(Minion):
    image_path = config['image']['minion5']
    image_size = (25, 50)
    max_health = 50
    speed = 75
    damage = 5
    attack_interval = 0.7
    cost = 15
    reward_xp = 25
    reward_cash = 25
    name = 'Knight'
    training_time = 2

    def __init__(self, x: float, player: int):
        super().__init__(x, player)

class Horse(Minion):
    image_path = config['image']['minion6']
    image_size = (25, 50)
    max_health = 80
    speed = 75
    damage = 7
    attack_interval = 0.9
    cost = 25
    reward_xp = 50
    reward_cash = 50
    name = 'Horse'
    training_time = 2.5

    def __init__(self, x: float, player: int):
        super().__init__(x, player)

class Soldier(Minion):
    image_path = config['image']['minion7']
    image_size = (25, 50)
    max_health = 120
    speed = 75
    damage = 10
    attack_interval = 0.4
    cost = 30
    reward_xp = 80
    reward_cash = 80
    name = 'Soldier'
    training_time = 2.5

    def __init__(self, x: float, player: int):
        super().__init__(x, player)

class Rambo(Minion):
    image_path = config['image']['minion8']
    image_size = (25, 50)
    max_health = 150
    speed = 75
    damage = 12
    attack_interval = 0.6
    cost = 50
    reward_xp = 120
    reward_cash = 120
    name = 'Rambo'
    training_time = 3

    def __init__(self, x: float, player: int):
        super().__init__(x, player)

class Tank(Minion):
    image_path = config['image']['minion9']
    image_size = (25, 50)
    max_health = 250
    speed = 75
    damage = 20
    attack_interval = 1.0
    cost = 80
    reward_xp = 180
    reward_cash = 180
    name = 'Tank'
    training_time = 3.5

    def __init__(self, x: float, player: int):
        super().__init__(x, player)

class Alien(Minion):
    image_path = config['image']['minion10']
    image_size = (25, 50)
    max_health = 300
    speed = 75
    damage = 30
    attack_interval = 0.4
    cost = 100
    reward_xp = 250
    reward_cash = 250
    name = 'Alien'
    training_time = 3.5

    def __init__(self, x: float, player: int):
        super().__init__(x, player)

class Robot(Minion):
    image_path = config['image']['minion11']
    image_size = (25, 50)
    max_health = 500
    speed = 75
    damage = 50
    attack_interval = 0.2
    cost = 150
    reward_xp = 350
    reward_cash = 350
    name = 'Robot'
    training_time = 4

    def __init__(self, x: float, player: int):
        super().__init__(x, player)

class UFO(Minion):
    image_path = config['image']['minion12']
    image_size = (25, 50)
    max_health = 1000
    speed = 75
    damage = 80
    attack_interval = 0.1
    cost = 250
    reward_xp = 500
    reward_cash = 500
    name = 'UFO'
    training_time = 5

    def __init__(self, x: float, player: int):
        super().__init__(x, player)

MINION_CHOICES = {
    0: {'spawn_1': Chimp,   'spawn_2': ClubMan, 'spawn_3': Dino},
    1: {'spawn_1': Jester,  'spawn_2': Knight,  'spawn_3': Horse},
    2: {'spawn_1': Soldier, 'spawn_2': Rambo,   'spawn_3': Tank},
    3: {'spawn_1': Alien,   'spawn_2': Robot,   'spawn_3': UFO},
}