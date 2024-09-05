import pygame
import json
from base import P1Base, P2Base
from game_object import HealthMixin
from ui import UI
from constants import BoxAction

with open('config.json', 'r') as file:
    config =  json.load(file)

DEBUG = config['debug']

class ObjectManager:

    def __init__(self, bases):
        self.objects = []

        self.bases = bases
        self.add_object(self.bases[1])
        self.add_object(self.bases[2])

        self.last_update_time = pygame.time.get_ticks()
        self.pressed_keys = set()

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        self.objects.remove(obj)

    def handle_ui_selections(self, ui_selections: list[tuple[int, BoxAction]]):
        for player, action in ui_selections:
            if action == BoxAction.EVOLVE:
                self.bases[player].try_evolve()
            elif action == BoxAction.TURRET_1:
                pass
            elif action == BoxAction.TURRET_2:
                pass
            elif action == BoxAction.POWER:
                pass


    def update_objects(self, pressed_keys: set, ui_selections: list[tuple[int, BoxAction]]):
        self.pressed_keys = pressed_keys
        current_time = pygame.time.get_ticks()
        self.delta = (current_time - self.last_update_time) / 1_000 # seconds
        for obj in self.objects:
            obj.update(self)
            if isinstance(obj, HealthMixin) and obj.health <= 0:
                self.handle_death(obj)

        self.last_update_time = current_time

        self.handle_ui_selections(ui_selections)

    def handle_death(self, obj):
        """Handle the death of an object, including removal and player rewards."""
        self.remove_object(obj)

        other_player = {1: 2, 2: 1}[obj.player]

        self.reward_player(other_player, obj.reward_xp, obj.reward_cash)

    def reward_player(self, player, xp, cash):
        self.bases[player].xp     += xp
        self.bases[player].budget += cash

    def draw_objects(self, screen):
        for obj in sorted(self.objects, key=lambda o: o.zorder):
            if obj.to_draw:
                obj.draw(screen)

                if isinstance(obj, HealthMixin):
                    obj.draw_health_bar(screen)

                if DEBUG:
                    obj.draw_collision_rect(screen)

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.screen_width  = config['screen_width']
        self.screen_height = config['screen_height']
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Age of War')

        self.bases = {1: P1Base(), 2: P2Base()}
        self.object_manager = ObjectManager(self.bases)

        self.background_image = pygame.transform.scale(
            pygame.image.load(config['image']['background']), (self.screen_width, self.screen_height)
        )   

        self.ui = UI(self.bases, self.screen, self.screen_width, self.screen_height)

    def run(self):
        running = True
        while running:
            pressed_keys = set()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    pressed_keys.add(event.key)

            self.screen.blit(self.background_image, (0, 0))

            ui_selections = self.ui.update(pressed_keys)
            self.ui.draw()

            self.object_manager.update_objects(pressed_keys, ui_selections)
            self.object_manager.draw_objects(self.screen)

            pygame.display.flip()

        pygame.quit()