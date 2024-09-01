import pygame
import sys

pygame.init()

screen_width = 1700
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Age of War')

background_image = pygame.image.load('assets/background.png')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.blit(background_image, (0, 0))
    
    pygame.display.flip()

pygame.quit()
sys.exit()
