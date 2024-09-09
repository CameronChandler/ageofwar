import pygame
import json
from base import P1Base, P2Base
from minion import Minion
from game_object import HealthMixin
from ui import UI
from constants import BoxAction, CONFIG_NAME, Color

with open(CONFIG_NAME, 'r') as file:
    config = json.load(file)

DEBUG = config['debug']

class ObjectManager:
    
    def __init__(self, bases):
        self.objects = []

        self.bases = bases
        self.add_object(self.bases[1])
        self.add_object(self.bases[2])

        # x tracks the actual x position, score tracks what this represents
        self.captured_ground_x = {1: self.bases[1].front_x, 2: self.bases[2].front_x}

        self.last_update_time = pygame.time.get_ticks()
        self.pressed_keys = set()

        self.screen_width = config['screen_width']
        self.screen_height = config['screen_height']

    def get_captured_ground_score(self, player: int):
        if player == 1:
            return self.captured_ground_x[1]
        return config['screen_width'] - self.captured_ground_x[2]

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        self.objects.remove(obj)
        del obj

    def handle_ui_selections(self, ui_selections: list[tuple[int, BoxAction]]):
        for player, action in ui_selections:
            if action == BoxAction.EVOLVE:
                self.bases[player].try_evolve()
            elif action == BoxAction.TURRET_1:
                self.bases[player].try_upgrade_turret(1)
            elif action == BoxAction.TURRET_2:
                self.bases[player].try_upgrade_turret(2)
            elif action == BoxAction.POWER:
                pass

    def update_captured_ground(self):
        """Update the captured ground based on minion positions."""
        furthest_minion = {p: self.bases[p].front_x for p in (1, 2)}
        for obj in self.objects:
            if isinstance(obj, Minion):
                if obj.player == 1:
                    furthest_minion[1] = max(obj.front_x, furthest_minion[1])
                else:
                    furthest_minion[2] = min(obj.front_x, furthest_minion[2])
                
        # Update with furthest minions
        self.captured_ground_x[1] = max(furthest_minion[1], self.captured_ground_x[1])
        self.captured_ground_x[2] = min(furthest_minion[2], self.captured_ground_x[2])

        # Account for minions capping opponent land
        if furthest_minion[1] > self.captured_ground_x[2]:
            self.captured_ground_x[2] = furthest_minion[1]

        elif furthest_minion[2] < self.captured_ground_x[1]:
            self.captured_ground_x[1] = furthest_minion[2]

    def is_off_screen(self, obj):
        threshold = 500  # Pixels off-screen threshold
        return (
            obj.x < -threshold or obj.x > self.screen_width  + threshold or
            obj.y < -threshold or obj.y > self.screen_height + threshold
        )

    def update_objects(self, pressed_keys: set, ui_selections: list[tuple[int, BoxAction]]):
        self.pressed_keys = pressed_keys
        current_time = pygame.time.get_ticks()
        self.delta = (current_time - self.last_update_time) / 1_000 # seconds
        for obj in self.objects:
            obj.update(self)
            if isinstance(obj, HealthMixin) and obj.health <= 0:
                self.handle_death(obj)

            if self.is_off_screen(obj):
                self.remove_object(obj)

        self.last_update_time = current_time

        self.handle_ui_selections(ui_selections)

        self.update_captured_ground()

    def handle_death(self, obj):
        """Handle the death of an object, including removal and player rewards."""
        self.remove_object(obj)

        other_player = {1: 2, 2: 1}[obj.player]

        self.reward_player(other_player, obj.reward_xp, obj.reward_cash)

    def reward_player(self, player, xp, cash):
        self.bases[player].xp     += xp
        self.bases[player].budget += cash

    def draw_captured_ground(self, screen):
        y = config['screen_height'] - config['ground_height'] 
        height = 10

        for player, color in [(1, Color.BLUE), (2, Color.RED)]:
            w2 = config['screen_width'] - self.get_captured_ground_score(player=2)
            box = {
                1: ( 0, y, self.captured_ground_x[1], height),
                2: (w2, y, self.get_captured_ground_score(player=2), height),
            }[player]
            #pygame.draw.rect(screen, color, box)

            surface = pygame.Surface((box[2], box[3]), pygame.SRCALPHA)
    
            surface.fill((*color, 192))  # RGBA
            screen.blit(surface, box)

    def draw_objects(self, screen):
        for obj in sorted(self.objects, key=lambda o: o.zorder):
            if obj.to_draw:
                obj.draw(screen)

                if isinstance(obj, HealthMixin):
                    obj.draw_health_bar(screen)

                if DEBUG:
                    obj.draw_collision_rect(screen)

        self.draw_captured_ground(screen)

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