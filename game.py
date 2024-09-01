import pygame
import json
from base import P1Base, P2Base

with open('config.json', 'r') as file:
    config =  json.load(file)

class ObjectManager:

    def __init__(self):
        self.objects = []
        self.last_update_time = pygame.time.get_ticks()

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        self.objects.remove(obj)

    def update_objects(self):
        current_time = pygame.time.get_ticks()
        delta = (current_time - self.last_update_time) / 1_000 # seconds
        for obj in self.objects:
            obj.update(self, delta)
        self.last_update_time = current_time

    def draw_objects(self, screen):
        for obj in self.objects:
            if obj.to_draw:
                obj.draw(screen)

        pygame.display.flip()

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width  = config['screen_width']
        self.screen_height = config['screen_height']
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Age of War')
        
        self.object_manager = ObjectManager()
        self.object_manager.add_object(P1Base())
        self.object_manager.add_object(P2Base())

        self.background_image = pygame.transform.scale(
            pygame.image.load(config['image']['background']), (self.screen_width, self.screen_height)
        )

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.blit(self.background_image, (0, 0))
            self.object_manager.update_objects()
            self.object_manager.draw_objects(self.screen)

        pygame.quit()