import pygame
from game_object import GameObject
import json
from typing import Optional
from math import atan2, degrees, copysign, sin, cos, radians
from projectile import Egg, Arrow, Bullet, Laser
from constants import CONFIG_NAME

with open(CONFIG_NAME, 'r') as file:
    config = json.load(file)

class Turret(GameObject):

    def __init__(self, x, y, player, angle):
        self.player = player
        
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, (self.image_size[0], self.image_size[1]))
        if self.player == 2:
            self.image = pygame.transform.flip(self.image, flip_x=False, flip_y=True)

        self.original_image = self.image.copy()
        
        self.x, self.y = x, y
        # if player 1, move turret back one length
        if self.player == 1:
            self.x -= self.image_size[0]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
        self.angle = angle if angle is not None else {1: 0, 2: 180}[self.player] 

        self.attack_interval = 1 / self.bullets_per_second
        self.time_to_attack = self.attack_interval

        super().__init__()
    
    @property
    def muzzle_position(self):
        """Calculate the position at the end of the turret barrel (muzzle) based on the angle."""
        # Get the turret's center
        center_x = self.rect.centerx
        center_y = self.rect.centery

        # Barrel length from center to muzzle (half the width of the turret)
        barrel_length = self.image_size[0] // 2

        # Calculate muzzle position using the turret's angle
        muzzle_x = center_x + barrel_length * cos(radians(self.angle))
        muzzle_y = center_y + barrel_length * sin(radians(self.angle))

        return muzzle_x, muzzle_y
    
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
    
    @property
    def damage(self):
        return self.dps / self.bullets_per_second

    def shoot(self, object_manager):
        muzzle_x, muzzle_y = self.muzzle_position
        object_manager.add_object(self.ProjectileClass(
            muzzle_x, muzzle_y, self.angle, self.player, self.damage
        ))

    def rotate_toward(self, target, delta):
        """Rotate the turret to point at the target and return the updated angle."""
        # Calculate the angle to the target in degrees
        dx = target.x - self.x
        dy = target.y - self.y + 7 # Aim a bit below target's center
        desired_angle = degrees(atan2(dy, dx))

        # Calculate the difference between the current angle and the target angle
        angle_diff = (desired_angle - self.angle) % 360
        if angle_diff > 180:
            angle_diff -= 360

        # Rotate by a fraction of the angle difference based on rotational velocity
        rotate_amount = self.rotational_velocity * delta
        angle = self.angle + copysign(min(abs(angle_diff), rotate_amount), angle_diff)

        return angle % 360
    
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

    @classmethod
    def load_attributes_from_config(cls):
        """Load static attributes for a specific minion type from the config."""
        cls.image_path = config['image'][cls.turret_id]
        cls.cost       = config['turret_stats'][cls.turret_id]['cost']
        cls.dps        = config['turret_stats'][cls.turret_id]['dps']

class EggLauncher(Turret):
    rotational_velocity = 60 # degrees/second
    turret_id = 'turret1'
    image_size = (60, 30)
    bullets_per_second = 0.5
    target_range = 450
    ProjectileClass = Egg

    def __init__(self, x: float, y: float, player: int, angle: int = 0):
        super().__init__(x, y, player, angle)

class Crossbow(Turret):
    rotational_velocity = 90 # degrees/second
    turret_id = 'turret2'
    image_size = (60, 30)
    bullets_per_second = 1
    target_range = 550
    ProjectileClass = Arrow

    def __init__(self, x: float, y: float, player: int, angle: int = 0):
        super().__init__(x, y, player, angle)

class MachineGun(Turret):
    rotational_velocity = 120 # degrees/second
    turret_id = 'turret3'
    image_size = (60, 30)
    bullets_per_second = 5
    target_range = 650
    ProjectileClass = Bullet

    def __init__(self, x: float, y: float, player: int, angle: int = 0):
        super().__init__(x, y, player, angle)

class LaserCannon(Turret):
    rotational_velocity = 180 # degrees/second
    turret_id = 'turret4'
    image_size = (60, 30)
    bullets_per_second = 10
    target_range = 750
    ProjectileClass = Laser

    def __init__(self, x: float, y: float, player: int, angle: int = 0):
        super().__init__(x, y, player, angle)

for cls in (EggLauncher, Crossbow, MachineGun, LaserCannon):
    cls.load_attributes_from_config()

TURRET_CHOICES = {
    0: EggLauncher, 
    1: Crossbow, 
    2: MachineGun, 
    3: LaserCannon
}