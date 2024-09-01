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
        self.minion_choices = {'spawn_1': Test, 'spawn_2': Test, 'spawn_3': Test}
        self.zorder = 100

    def take_damage(self, amount):
        self.health -= amount

    def is_destroyed(self):
        return self.health <= 0

    def _check_player_input(self, object_manager):
        for key in ['spawn_1', 'spawn_2', 'spawn_3']:
            if CONTROLS[self.player][key] in object_manager.pressed_keys:
                object_manager.add_object(self.minion_choices[key](self.x, self.y + BASE_HEIGHT, self.player))
                break

    def update(self, object_manager):
        self._check_player_input(object_manager)

class P1Base(Base):
    def __init__(self):
        super().__init__(player=1)

class P2Base(Base):
    def __init__(self):
        super().__init__(player=2)
