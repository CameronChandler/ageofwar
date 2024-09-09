import pygame
import json
from base import P1Base, P2Base
from minion import Minion
from game_object import HealthMixin
from ui import UI
from constants import BoxAction, CONFIG_NAME, Color

with open(CONFIG_NAME, 'r') as file:
    config = json.load(file)

class TerritoryManager:

    def __init__(self, base1_x, base2_x):
        self.territory = {
            1: Territory(base1_x, player=1), 
            2: Territory(base2_x, player=2)
        }

    def get_furthest_minion_x(self, objects: list) -> dict[int: int]:
        furthest_minion_x = {p: self.territory[p].base_x for p in (1, 2)}
        for obj in objects:
            if isinstance(obj, Minion):
                if obj.player == 1:
                    furthest_minion_x[1] = max(obj.front_x, furthest_minion_x[1])
                else:
                    furthest_minion_x[2] = min(obj.front_x, furthest_minion_x[2])

        return furthest_minion_x

    def update(self, object_manager):
        """Update the captured ground based on minion positions."""
        furthest_minion_x = self.get_furthest_minion_x(object_manager.objects)

        # Update with furthest minions
        self.territory[1].cap_x = max(furthest_minion_x[1], self.territory[1].cap_x)
        self.territory[2].cap_x = min(furthest_minion_x[2], self.territory[2].cap_x)

        # Account for minions capping opponent land
        if furthest_minion_x[1] > self.territory[2].cap_x:
            self.territory[2].cap_x = furthest_minion_x[1]

        elif furthest_minion_x[2] < self.territory[1].cap_x:
            self.territory[1].cap_x = furthest_minion_x[2]

    def draw(self, screen):
        for territory in self.territory.values():
            territory.draw(screen)


class Territory:
    y = config['screen_height'] - config['ground_height'] 
    height = 10

    def __init__(self, base_x, player):
        ''' base_x is the "front" of the base '''
        self.player = player
        self.base_x = base_x
        self.cap_x = base_x
        self.color = {
            'default': Color.BLUE        if player == 1 else Color.RED,
            'bright' : Color.BRIGHT_BLUE if player == 1 else Color.BRIGHT_RED
        }

    def get_captured_ground_score(self):
        """Return the current captured ground score for the player."""
        if self.player == 1:
            return self.cap_x
        return config['screen_width'] - self.cap_x
    
    def draw(self, screen):
        if self.player == 1:
            box = (0, self.y, self.cap_x, self.height)
        else:
            w2 = config['screen_width'] - self.get_captured_ground_score()
            box = (w2, self.y, self.get_captured_ground_score(), self.height)

        surface = pygame.Surface((box[2], box[3]), pygame.SRCALPHA)

        surface.fill((*self.color['default'], 192))  # RGBA
        screen.blit(surface, box)