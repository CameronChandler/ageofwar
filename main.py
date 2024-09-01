import pygame
import sys
import json
from base import P1Base, P2Base

with open('config.json', 'r') as file:
    config =  json.load(file)

pygame.init()

screen_width  = config['screen_width']
screen_height = config['screen_height']
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Age of War')

background_image = pygame.image.load('assets/background.png')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

p1_base = P1Base()
p2_base = P2Base()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.blit(background_image, (0, 0))
    p1_base.draw(screen)
    p2_base.draw(screen)
    
    pygame.display.flip()

pygame.quit()
sys.exit()
