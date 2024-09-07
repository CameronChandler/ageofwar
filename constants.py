import pygame
from enum import Enum

CONFIG_NAME = 'test_config.json'

class ValueEnum(Enum):
    ''' Enums that return the value you assign them '''
    def __get__(self, instance, owner):
        return self.value

class Color(ValueEnum):
    WHITE  = (255, 255, 255)
    RED    = (255,   0,   0)
    GREEN  = (  0, 255,   0)
    YELLOW = (255, 255,   0)
    GREY   = (100, 100, 100)
    
class BoxAction(ValueEnum):
    EVOLVE = 'Evolve'
    POWER = 'Power'
    TURRET_1 = 'Turret 1'
    TURRET_2 = 'Turret 2'

P1_KEYS = {'up': pygame.K_w , 'down': pygame.K_s   , 'left': pygame.K_a   , 'right': pygame.K_d}
P2_KEYS = {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT}