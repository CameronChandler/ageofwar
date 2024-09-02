import pygame
import json
from game_object import GameObject
from minion import Test1, Test2, Test3

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
        'spawn_3': pygame.K_SLASH,
    }
}

MINION_CHOICES = {
    0: {'spawn_1': Test1, 'spawn_2': Test2, 'spawn_3': Test3},
}

BASE_WIDTH  = 100
BASE_HEIGHT = 100

class Base(GameObject):
    max_queue_length = 5

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
        self.zorder = 100
        self.budget = 10
        self.evolution = 0

        self.training_queue = []
        self.elapsed_training_time = 0

    @property
    def minion_choices(self):
        return MINION_CHOICES[self.evolution]
    
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

    def _process_training_queue(self, object_manager):
        if not self.training_queue:
            return

        minion_class = self.training_queue[0]
        self.elapsed_training_time += object_manager.delta
        if self.elapsed_training_time >= minion_class.training_time:
            object_manager.add_object(minion_class(self.x, self.player))
            self.elapsed_training_time = 0
            self.training_queue.pop(0)

    def create_minion(self, minion_class):
        minion = minion_class(self.x, self.player)
        # Replace with actual logic to add the minion to the game
        print(f"Minion created: {minion}")

    def get_training_queue_status(self) -> tuple[int, float]:
        queue_length = len(self.training_queue)
        queue_progress = 0
        if queue_length > 0:
            current_minion_class = self.training_queue[0]
            queue_progress = self.elapsed_training_time / current_minion_class.training_time
        return queue_length, queue_progress

class P1Base(Base):
    def __init__(self):
        super().__init__(player=1)

class P2Base(Base):
    def __init__(self):
        super().__init__(player=2)
