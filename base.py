import pygame
import json
from game_object import GameObject
from minion import Test

with open('config.json', 'r') as file:
    config =  json.load(file)

CONTROLS = {
    1: {
        'spawn_1': pygame.K_1,
        'spawn_2': pygame.K_2,
        'spawn_3': pygame.K_3,
    },
    2: {
        'spawn_1': pygame.K_COMMA,
        'spawn_2': pygame.K_PERIOD,
        'spawn_3': pygame.K_BACKSLASH,
    }
}

BASE_WIDTH  = 100
BASE_HEIGHT = 100

class Base(GameObject):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.health = config['base_health']
        self.image = pygame.image.load(config['image']['base'])
        self.image = pygame.transform.scale(self.image, (BASE_WIDTH, BASE_HEIGHT))
        self.rect = self.image.get_rect()
        self.x = 0 if player == 1 else config['screen_width'] - BASE_WIDTH
        self.y = config['screen_height'] - BASE_HEIGHT - config['ground_height']
        self.rect.topleft = (self.x, self.y)
        self.minions = []

    def take_damage(self, amount):
        self.health -= amount

    def is_destroyed(self):
        return self.health <= 0

    def _check_player_input(self, object_manager, delta):
        keys = pygame.key.get_pressed()
        if keys[CONTROLS[self.player]['spawn_1']]:
            object_manager.add_object(Test(self.x, self.y - BASE_HEIGHT, self.player))
        elif keys[CONTROLS[self.player]['spawn_2']]:
            pass

    def update(self, object_manager, delta):
        self._check_player_input(object_manager, delta)

class P1Base(Base):
    def __init__(self):
        super().__init__(player=1)

class P2Base(Base):
    def __init__(self):
        super().__init__(player=2)
