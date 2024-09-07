import pygame
from game_object import GameObject
import json
from typing import Optional
from math import atan2, degrees, copysign
from projectile import Projectile1

with open('config.json', 'r') as file:
    config = json.load(file)

class Turret(GameObject):
    rotational_velocity = 90 # degrees/second

    def __init__(self, x, y, player):
        self.player = player
        
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, (self.image_size[0], self.image_size[1]))
        self.original_image = self.image.copy()
        
        self.x, self.y = x, y
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        
        self.angle = 0
        if self.player == 2:
            self.angle += 180
            self.speed = -self.speed
            self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)

        self.attack_interval = 1 / self.bullets_per_second
        self.time_to_attack = self.attack_interval

        super().__init__()

    @property
    def name():
        raise NotImplementedError

    @property
    def ProjectileClass():
        raise NotImplementedError

    @property
    def cost():
        raise NotImplementedError

    @property
    def training_time():
        raise NotImplementedError

    @property
    def bullets_per_second():
        raise NotImplementedError

    @property
    def target_range():
        raise NotImplementedError
    
    def distance(self, obj1, obj2):
        return ((obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2) ** 0.5

    def find_nearest_enemy(self, object_manager) -> Optional[GameObject]:
        """Find the nearest enemy within a certain range."""
        nearest_enemy = None
        nearest_distance = float('inf')

        for obj in object_manager.objects:
            parent_class_name = str(type(obj).__bases__)
            if not 'Minion' in parent_class_name and not 'Base' in parent_class_name:
                continue
            
            if obj.player != self.player:
                distance = self.distance(self, obj)
                if (distance < nearest_distance) & (distance < self.target_range):
                    nearest_distance = distance
                    nearest_enemy = obj

        return nearest_enemy

    def shoot(self, object_manager):
        object_manager.add_object(self.ProjectileClass(self.x, self.y, self.angle, self.player))

    def rotate_toward(self, target, delta):
        """Rotate the turret to point at the target and return the updated angle."""
        # Calculate the angle to the target in degrees
        dx = target.x - self.x
        dy = target.y - self.y
        desired_angle = degrees(atan2(dy, dx))

        # Calculate the difference between the current angle and the target angle
        angle_diff = (desired_angle - self.angle) % 360
        if angle_diff > 180:
            angle_diff -= 360

        # Rotate by a fraction of the angle difference based on rotational velocity
        rotate_amount = self.rotational_velocity * delta  # Amount to rotate this frame
        self.angle += copysign(min(abs(angle_diff), rotate_amount), angle_diff)  # Adjust current angle gradually

        # Keep the angle between 0 and 360 degrees
        self.angle %= 360

        # Return the updated angle
        return self.angle
    
    def draw(self, screen):
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=(self.center_x, self.center_y))
        super().draw(screen)
    
    def update(self, object_manager):
        nearest_enemy = self.find_nearest_enemy(object_manager)
        if nearest_enemy is None:
            return

        # Rotate to face the nearest enemy
        self.angle = self.rotate_toward(nearest_enemy, object_manager.delta)

        # Check if it's time to attack
        if self.time_to_attack <= 0:
            self.shoot(object_manager)
            self.time_to_attack = self.attack_interval
        else:
            self.time_to_attack -= object_manager.delta

class Turret1(Turret):
    image_path = config['image']['turret1']
    image_size = (60, 10)
    max_health = 100
    speed = 100
    damage = 10
    bullets_per_second = 1
    cost = 1
    reward_xp = 1
    reward_cash = 1
    name = 'Turret1'
    training_time = 2
    target_range = 500
    ProjectileClass = Projectile1

    def __init__(self, x: float, y: float, player: int):
        super().__init__(x, y, player)