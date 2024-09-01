import pygame
import json

with open('config.json', 'r') as file:
    config =  json.load(file)

BASE_WIDTH  = 100
BASE_HEIGHT = 100

class Base:
    def __init__(self, player):
        self.player = player
        self.health = config['base_health']
        self.image = pygame.image.load('./assets/base.png')
        self.image = pygame.transform.scale(self.image, (BASE_WIDTH, BASE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0 if player == 1 else config['screen_width'] - BASE_WIDTH, config['screen_height'] - BASE_HEIGHT - config['ground_height'])

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def take_damage(self, amount):
        self.health -= amount

    def is_destroyed(self):
        return self.health <= 0

class P1Base(Base):
    def __init__(self):
        super().__init__(player=1)

class P2Base(Base):
    def __init__(self):
        super().__init__(player=2)
