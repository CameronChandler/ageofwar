import pygame
import json
from minion import Minion
from constants import CONFIG_NAME, Color
from math import exp, cos, pi

with open(CONFIG_NAME, 'r') as file:
    config = json.load(file)


class TerritoryManager:
    reward_interval = 7 # seconds
    max_captured = config['screen_width']

    def __init__(self, base1_x, base2_x):
        self.territory = {
            1: Territory(base1_x, player=1), 
            2: Territory(base2_x, player=2)
        }
        self.time_to_reward = self.reward_interval
        self.time_elapsed = 0

    @property
    def pulse_strength(self):
        # max avoids first pulse
        x = max(self.reward_interval/2, self.time_elapsed)
        return cos(pi * x / self.reward_interval) ** 150

    @property
    def base_reward(self, a=0.023, b=0.2):
        ''' Reward for owning the whole screen '''
        return exp(a*self.time_elapsed) + b*self.time_elapsed
    
    def reward(self, object_manager):
        for player in (1, 2):
            captured = self.territory[player].get_captured_ground_score()
            prop_captured = captured / self.max_captured
            reward = max(1, int(prop_captured * self.base_reward))
            object_manager.reward_player(player, xp=0, cash=reward)
    
    def handle_rewards(self, object_manager):
        self.time_elapsed += object_manager.delta
        self.time_to_reward -= object_manager.delta

        if self.time_to_reward < 0:
            self.reward(object_manager)
            print(f'Base Reward: {self.base_reward}, Time: {self.time_elapsed}')
            self.time_to_reward = self.reward_interval

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
        #### Note that currently minions don't cap past base because
        #### the base is counted as the furthest minion,
        #### so these equalities won't allow attacker color to be drawn
        #### Would need to add case for victory or being past base_x
        if furthest_minion_x[1] > self.territory[2].cap_x:
            self.territory[2].cap_x = furthest_minion_x[1]

        if furthest_minion_x[2] < self.territory[1].cap_x:
            self.territory[1].cap_x = furthest_minion_x[2]
            
        # Handle rewards
        self.handle_rewards(object_manager)

    def draw(self, screen):
        for territory in self.territory.values():
            territory.draw(screen, self.pulse_strength)


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
        score = self.cap_x if self.player == 1 else config['screen_width'] - self.cap_x
        return max(0, score)
    
    def interpolate_color(self, c1, c2, factor):
        return tuple(
            int(c1[i] + (c2[i] - c1[i]) * factor) for i in range(3)
        )
    
    def draw(self, screen, pulse_strength: float):
        ''' Pulse strength in [0, 1] '''
        if self.player == 1:
            box = (0, self.y, self.cap_x, self.height)
        else:
            w2 = config['screen_width'] - self.get_captured_ground_score()
            box = (w2, self.y, self.get_captured_ground_score(), self.height)

        surface = pygame.Surface((box[2], box[3]), pygame.SRCALPHA)

        pulse_color = self.interpolate_color(
            self.color['default'], self.color['bright'], pulse_strength
        )

        surface.fill((*pulse_color, 192))  # RGBA
        screen.blit(surface, box)