import pygame
import json
from base import P1Base, P2Base

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

    def update_objects(self):
        current_time = pygame.time.get_ticks()
        self.delta = (current_time - self.last_update_time) / 1_000 # seconds
        for obj in self.objects:
            obj.update(self)
        self.last_update_time = current_time

    def draw_objects(self, screen):
        for obj in sorted(self.objects, key=lambda o: o.zorder):
            if obj.to_draw:
                obj.draw(screen)

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)

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

    def draw_budget(self):
        budget_text_p1 = self.font.render(f'P1 Budget: ${self.bases[1].budget}', True, (255, 255, 255))
        self.screen.blit(budget_text_p1, (10, 10))

        budget_text_p2 = self.font.render(f'P2 Budget: ${self.bases[2].budget}', True, (255, 255, 255))
        text_rect = budget_text_p2.get_rect(topright=(self.screen_width - 10, 10))
        self.screen.blit(budget_text_p2, text_rect)

    def run(self):
        running = True
        while running:
            pressed_keys = set()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    pressed_keys.add(event.key)

            self.object_manager.pressed_keys = pressed_keys

            self.screen.blit(self.background_image, (0, 0))
            self.object_manager.update_objects()
            self.object_manager.draw_objects(self.screen)
            self.draw_budget()

            pygame.display.flip()

        pygame.quit()