import pygame
import json
from game_object import GameObject, HealthMixin
from minion import MINION_CHOICES
from turret import TURRET_CHOICES
from constants import CONFIG_NAME

with open(CONFIG_NAME, 'r') as file:
    config = json.load(file)

CONTROLS = {
    1: {
        'spawn_1': pygame.K_1,
        'spawn_2': pygame.K_2,
        'spawn_3': pygame.K_3,
    },
    2: {
        'spawn_1': pygame.K_COMMA,
        'spawn_2': pygame.K_PERIOD,
        'spawn_3': pygame.K_SLASH,
    }
}

EVOLUTION_COST = config['evolution_costs']

class Base(GameObject, HealthMixin):
    max_queue_length = 5
    inflate_pixels = 70
    reward_xp = 1e6
    reward_cash = 1e6
    offset = 10
    image_size = (100, 100)
    max_health = 100

    def __init__(self, player):
        self.player = player
        self.health = self.max_health
        self.image = pygame.image.load(config['image']['base'])
        self.image = pygame.transform.scale(self.image, (self.image_size[0], self.image_size[1]))
        self.rect = self.image.get_rect()

        self.x = {1: self.offset, 2: config['screen_width'] - self.image_size[0] - self.offset}[self.player]
        self.y = config['screen_height'] - self.image_size[1] - config['ground_height']
        self.rect.topleft = (self.x, self.y)
        self.zorder = 100
        self.budget = 10
        self.xp = 0
        self.evolution = 0

        self.training_queue = []
        self.elapsed_training_time = 0

        self.turrets = {1: None, 2: None}
        self.turret_x = self.x
        if self.player == 1:
            self.turret_x += self.image_size[0]
        self.turret_y = {1: self.y - 100, 2: self.y - 50}

        super().__init__()

    @property
    def start_x(self):
        return {
            1: Base.image_size[0] + Base.offset,
            2: config['screen_width'] - Base.image_size[0] - Base.offset
        }[self.player]

    @property
    def minion_choices(self):
        return MINION_CHOICES[self.evolution]

    @property
    def turret_choice(self):
        return TURRET_CHOICES[self.evolution]
    
    @property
    def can_evolve(self):
        if self.evolution >= len(EVOLUTION_COST):
            return False
        return EVOLUTION_COST[self.evolution] <= self.xp
    
    def try_evolve(self):
        if self.can_evolve:
            self.evolution += 1
    
    def try_spawn(self, object_manager, minion):
        if self.budget >= minion.cost:
            object_manager.add_object(minion)
            self.budget -= minion.cost
        else:
            del minion

    def try_enqueue(self, minion_class):
        if self.budget >= minion_class.cost and len(self.training_queue) < self.max_queue_length:
            self.training_queue.append(minion_class)
            self.budget -= minion_class.cost

    def _check_player_input(self, object_manager):
        for key in ['spawn_1', 'spawn_2', 'spawn_3']:
            if CONTROLS[self.player][key] in object_manager.pressed_keys:
                minion_class = self.minion_choices[key]
                self.try_enqueue(minion_class)
                break

    def update(self, object_manager):
        self._check_player_input(object_manager)
        self._process_training_queue(object_manager)

        for turret in self.turrets.values():
            if turret is not None:
                turret.update(object_manager)

    def draw(self, screen):
        for turret in self.turrets.values():
            if turret is not None:
                turret.draw(screen)

        super().draw(screen)

    def _process_training_queue(self, object_manager):
        if not self.training_queue:
            return

        minion_class = self.training_queue[0]
        self.elapsed_training_time += object_manager.delta
        if self.elapsed_training_time >= minion_class.training_time:
            object_manager.add_object(minion_class(self.x + self.image_size[0]/2, self.player))
            self.elapsed_training_time = 0
            self.training_queue.pop(0)

    def get_training_queue_status(self) -> tuple[int, float]:
        queue_length = len(self.training_queue)
        queue_progress = 0
        if queue_length > 0:
            current_minion_class = self.training_queue[0]
            queue_progress = self.elapsed_training_time / current_minion_class.training_time
        return queue_length, queue_progress
    
    def get_turret_cost(self, turret: int) -> int:
        NewTurretClass = TURRET_CHOICES[self.evolution]
        current_cost = 0 if self.turrets[turret] is None else self.turrets[turret].cost
        return NewTurretClass.cost - current_cost
    
    def can_upgrade_turret(self, turret: int):
        NewTurretClass = TURRET_CHOICES[self.evolution]
        current_turret_is_worse = self.turrets[turret].__class__ != NewTurretClass
        can_afford = self.budget - self.get_turret_cost(turret) >= 0

        return current_turret_is_worse and can_afford
    
    def try_upgrade_turret(self, turret: int):
        NewTurretClass = TURRET_CHOICES[self.evolution]

        if self.can_upgrade_turret(turret):
            self.budget -= self.get_turret_cost(turret)
            
            angle = None
            if self.turrets[turret] is not None:
                angle = self.turrets[turret].angle

            del self.turrets[turret]
            self.turrets[turret] = NewTurretClass(self.turret_x, self.turret_y[turret], self.player, angle)

class P1Base(Base):
    def __init__(self):
        super().__init__(player=1)

class P2Base(Base):
    def __init__(self):
        super().__init__(player=2)
