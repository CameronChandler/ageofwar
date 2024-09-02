import pygame
import json
from base import Base, P1Base, P2Base
from constants import Color

with open('config.json', 'r') as file:
    config =  json.load(file)

class ObjectManager:

    def __init__(self):
        self.objects = []
        self.last_update_time = pygame.time.get_ticks()
        self.pressed_keys = set()

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        self.objects.remove(obj)

    def update_objects(self, pressed_keys: set):
        self.pressed_keys = pressed_keys
        current_time = pygame.time.get_ticks()
        self.delta = (current_time - self.last_update_time) / 1_000 # seconds
        for obj in self.objects:
            obj.update(self)
        self.last_update_time = current_time

    def draw_objects(self, screen):
        for obj in sorted(self.objects, key=lambda o: o.zorder):
            if obj.to_draw:
                obj.draw(screen)

class UI:

    def __init__(self, bases, screen, screen_width, screen_height):
        self.bases = bases
        self.screen = screen
        self.screen_width  = screen_width
        self.screen_height = screen_height

        self.font = pygame.font.Font(None, 36)

    def draw_budget(self):
        budget_text_p1 = self.font.render(f'P1 Budget: ${self.bases[1].budget}', True, Color.WHITE)
        self.screen.blit(budget_text_p1, (10, 10))

        budget_text_p2 = self.font.render(f'P2 Budget: ${self.bases[2].budget}', True, Color.WHITE)
        text_rect = budget_text_p2.get_rect(topright=(self.screen_width - 10, 10))
        self.screen.blit(budget_text_p2, text_rect)

    def draw_training_queue(self, queue_length, queue_progress, x, y, total_length, height):
        edge_width = 4
        num_squares = Base.max_queue_length
        # Gap between squares required to make slots length = total_length
        gap = (total_length - num_squares*height) / (num_squares - 1)

        for i in range(num_squares):
            slot_rect = pygame.Rect(x + i * (height + gap), y, height, height)
            # If 0, makes filled square, if int it is edge width
            edge_width_or_no_fill = edge_width if i >= queue_length else 0
            pygame.draw.rect(self.screen, Color.WHITE, slot_rect, edge_width_or_no_fill)

        loading_bar_width = int(total_length * queue_progress)
        loading_bar_rect = pygame.Rect(x, y + gap + height, loading_bar_width, gap)
        pygame.draw.rect(self.screen, Color.WHITE, loading_bar_rect)

    def draw_training_queues(self):
        total_length = 150
        height = 20

        p1_x = 10
        p1_y = 50 

        p2_x = self.screen_width - total_length - 10
        p2_y = 50

        queue_length, queue_progress = self.bases[1].get_training_queue_status()
        self.draw_training_queue(queue_length, queue_progress, p1_x, p1_y, total_length, height)

        queue_length, queue_progress = self.bases[2].get_training_queue_status()
        self.draw_training_queue(queue_length, queue_progress, p2_x, p2_y, total_length, height)

    def draw(self):
        self.draw_budget()
        self.draw_training_queues()

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.screen_width  = config['screen_width']
        self.screen_height = config['screen_height']
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Age of War')

        self.object_manager = ObjectManager()
        self.bases = {1: P1Base(), 2: P2Base()}
        self.object_manager.add_object(self.bases[1])
        self.object_manager.add_object(self.bases[2])

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
            self.object_manager.update_objects(pressed_keys)
            self.object_manager.draw_objects(self.screen)
            self.ui.draw()

            pygame.display.flip()

        pygame.quit()