import json
from projectile import PowerRock, PowerArrow, PowerBomb, PowerLaser
from ui import BoxAction
from constants import CONFIG_NAME, BoxAction
import random
import math

with open(CONFIG_NAME, 'r') as file:
    config = json.load(file)

GROUND_Y = config['screen_height'] - config['ground_height'] 


def poisson_disc_1d(min_dist, n_points, num_attempts=30):
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


class Spawner:
    lifetime = 7

    def __init__(self, player: int, min_range: int, max_range: int):
        self.player = player
        self.time_elapsed = 0
        self.spawn_interval = self.lifetime / (self.num_projectiles + 1)
        self.time_to_spawn = self.spawn_interval

        min_dist = 1 / (2*self.num_projectiles)
        self.xs = poisson_disc_1d(min_dist, self.num_projectiles+1)
        self.min_range = min_range
        self.max_range = max_range

        self.num_spawned = 0

    def update(self, object_manager):
        self.time_to_spawn -= object_manager.delta

        if self.time_to_spawn < 0:
            self.spawn(object_manager)
            self.time_to_spawn = self.spawn_interval

        self.time_elapsed += object_manager.delta

    def scale(self, value, a, b):
        """
        Scales a value from the range [0, 1] to the range [a, b].

        Parameters:
        value (float): The value in the range [0, 1].
        a (float): The lower bound of the target range.
        b (float): The upper bound of the target range.

        Returns:
        float: The scaled value in the range [a, b].
        """
        return a + (value * (b - a))

    def spawn(self, object_manager):
        x = self.scale(self.xs[self.num_spawned], self.min_range, self.max_range)
        projectile = self.ProjectileClass(x, self.player)
        object_manager.add_object(projectile)

        self.num_spawned += 1


class VolcanoSpawner(Spawner):
    ProjectileClass = PowerRock
    num_projectiles = 5

    def __init__(self, player: int, min_range: int, max_range: int):
        super().__init__(player, min_range, max_range)


class ArrowSpawner(Spawner):
    ProjectileClass = PowerArrow
    num_projectiles = 10

    def __init__(self, player: int, min_range: int, max_range: int):
        super().__init__(player, min_range, max_range)


class BombSpawner(Spawner):
    ProjectileClass = PowerBomb
    num_projectiles = 20

    def __init__(self, player: int, min_range: int, max_range: int):
        super().__init__(player, min_range, max_range)


class LaserSpawner(Spawner):
    ProjectileClass = PowerLaser
    num_projectiles = 30

    def __init__(self, player: int, min_range: int, max_range: int):
        super().__init__(player, min_range, max_range)


class PowerManager:
    spawner_choices = [VolcanoSpawner, ArrowSpawner, BombSpawner, LaserSpawner]
    power_interval = 30

    def __init__(self, min_range: int, max_range: int):
        self.time_to_power = {1: self.power_interval, 2: self.power_interval}
        self.active_spawners = {1: None, 2: None}
        self.min_range = min_range
        self.max_range = max_range

    @property
    def ready_status(self):
        return {p: self.time_to_power[p] <= 0 for p in (1, 2)}

    def try_spawn_power(self, SpawnerClass, player: int):
        if self.time_to_power[player] < 0:
            self.active_spawners[player] = SpawnerClass(
                player, self.min_range, self.max_range
            )
            self.time_to_power[player] = self.power_interval

    def update(self, ui_selections: list[tuple[int, BoxAction]], object_manager):
        for player, action in ui_selections:
            if action == BoxAction.POWER:
                evolution = object_manager.bases[player].evolution
                SpawnerClass = self.spawner_choices[evolution]
                self.try_spawn_power(SpawnerClass, player)

        for player in (1, 2):
            spawner = self.active_spawners[player]
            if spawner is not None:
                spawner.update(object_manager)
                
                if spawner.time_elapsed > spawner.lifetime:
                    del spawner
                    self.active_spawners[player] = None

            self.time_to_power[player] -= object_manager.delta

            # This is probably the worst code in the repo:
            object_manager.bases[player].power_ready = self.ready_status[player]

        