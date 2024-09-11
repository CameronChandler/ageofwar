import pygame
from enum import Enum

CONFIG_NAME = 'test_config.json'

class ValueEnum(Enum):
    ''' Enums that return the value you assign them '''
    def __get__(self, instance, owner):
        return self.value

class Color(ValueEnum):
    WHITE       = (255, 255, 255)
    RED         = (255,   0,   0)
    BRIGHT_RED  = (255, 100,   0)
    GREEN       = (  0, 255,   0)
    BLUE        = (  0,   0, 255)
    BRIGHT_BLUE = (  0, 150, 255)
    YELLOW      = (255, 255,   0)
    GREY        = (100, 100, 100)
    
class BoxAction(ValueEnum):
    EVOLVE = 'Evolve'
    POWER  = 'Power'
    TURRET_1 = 'Turret 1'
    TURRET_2 = 'Turret 2'

P1_KEYS = {'up': pygame.K_w , 'down': pygame.K_s   , 'left': pygame.K_a   , 'right': pygame.K_d}
P2_KEYS = {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT}







import json
from projectile import PowerRock, PowerArrow, PowerBomb, PowerLaser
from ui import BoxAction
from constants import CONFIG_NAME, BoxAction
import random
import math

with open(CONFIG_NAME, 'r') as file:
    config = json.load(file)

GROUND_Y = config['screen_height'] - config['ground_height'] 


def poisson_disc_1d(min_dist, num_attempts=30, n_points=10):
    # Initialize an empty list for storing the sample points
    samples = []

    # Start by choosing an initial random point in the domain [0, 1]
    initial_point = random.uniform(0, 1)
    samples.append(initial_point)
    
    # Create a list to hold points that are "active" (i.e., points around which new points can be sampled)
    active_list = [initial_point]

    # Continue until we have the desired number of points
    while len(samples) < n_points:
        if not active_list:
            # If we run out of active points, but haven't reached the required n_points, stop
            break
        
        # Pick a random active point
        current_point = random.choice(active_list)

        # Try to generate a valid new point around the current point
        found_new_point = False
        for _ in range(num_attempts):
            # Generate an offset that ensures the new point is within the [0, 1] range
            offset = random.uniform(min_dist, 3 * min_dist) * random.choice([-1, 1])
            new_point = current_point + offset
            
            # Ensure the new point is within the valid domain [0, 1]
            if new_point < 0 or new_point > 1:
                continue

            # Check if the new point is at least min_dist away from all other points
            if all(math.fabs(new_point - existing_point) >= min_dist for existing_point in samples):
                samples.append(new_point)
                active_list.append(new_point)
                found_new_point = True
                break

        # If no valid point was found after all attempts, remove the current point from the active list
        if not found_new_point:
            active_list.remove(current_point)

    # Sort and return exactly n points (in case more were generated)
    output = samples[:n_points]
    random.shuffle(output)
    return output

