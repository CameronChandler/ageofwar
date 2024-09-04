import pygame
import json
from base import Base, P1Base, P2Base
from constants import Color
from game_object import HealthMixin

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

    def update_objects(self, pressed_keys: set):
        self.pressed_keys = pressed_keys
        current_time = pygame.time.get_ticks()
        self.delta = (current_time - self.last_update_time) / 1_000 # seconds
        for obj in self.objects:
            obj.update(self)
            if isinstance(obj, HealthMixin) and obj.health <= 0:
                self.handle_death(obj)

        self.last_update_time = current_time

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

# class Box:
#     def __init__(self, x, y, player):
#         self.x = x
#         self.y = y
#         self.player = player
#         self.rect = pygame.Rect(x, y, 50, 50)  # Adjust size as needed
#         self.selected = False

#     def draw(self, screen):
#         color = Color.YELLOW if self.selected else Color.GREY
#         pygame.draw.rect(screen, color, self.rect, 2)

class UI:

    def __init__(self, bases, screen, screen_width, screen_height):
        self.bases = bases
        self.screen = screen
        self.screen_width  = screen_width
        self.screen_height = screen_height

        self.font = pygame.font.Font(None, 36)

        # self.boxes = {
        #     1: [Box(100 +                     i * 60     , self.screen_height - 100, 1) for i in range(3)],
        #     2: [Box(self.screen_width - 100 - i * 60 - 50, self.screen_height - 100, 2) for i in range(3)]
        # }

        # self.selected_boxes = {1: 0, 2: 0}

    def draw_minion_choices(self):
        for player in (1, 2):
            minion_choices = list(self.bases[player].minion_choices.values())
            box_width = 50
            padding = 20
            
            for i, minion_type in enumerate(minion_choices):
                image = pygame.image.load(minion_type.image_path)
                rect = image.get_rect(topleft=(0, 0))
                original_length = max(rect.width, rect.height)
                new_size = (
                    (0.8 * box_width * rect.width ) // original_length,
                    (0.8 * box_width * rect.height) // original_length
                )

                image = pygame.transform.scale(image, new_size)
                x = 380
                offset = (x if player == 1 else self.screen_width - x - len(minion_choices)*(box_width + padding))
                box_x = offset + i*(box_width + padding)
                box_y = 10
                image_x = box_x + (box_width - new_size[0]) // 2
                image_y = box_y + (box_width - new_size[1]) // 2
                self.screen.blit(image, (image_x, image_y))

                pygame.draw.rect(self.screen, Color.GREY, (box_x, box_y, box_width, box_width), 4)

    def draw_budget(self):
        x_pos = 50
        budget_text_p1 = self.font.render(f'Budget: ${self.bases[1].budget}', True, Color.WHITE)
        self.screen.blit(budget_text_p1, (x_pos, 10))

        budget_text_p2 = self.font.render(f'Budget: ${self.bases[2].budget}', True, Color.WHITE)
        text_rect = budget_text_p2.get_rect(topright=(self.screen_width - x_pos, 10))
        self.screen.blit(budget_text_p2, text_rect)

    def draw_xp(self):
        x_pos = 250
        xp_text_p1 = self.font.render(f'XP: {self.bases[1].xp}', True, Color.WHITE)
        self.screen.blit(xp_text_p1, (x_pos, 10))

        xp_text_p2 = self.font.render(f'XP: {self.bases[2].xp}', True, Color.WHITE)
        text_rect = xp_text_p2.get_rect(topright=(self.screen_width - x_pos, 10))
        self.screen.blit(xp_text_p2, text_rect)

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
        self.draw_xp()
        self.draw_minion_choices()
        self.draw_training_queues()

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
            self.object_manager.update_objects(pressed_keys)
            self.object_manager.draw_objects(self.screen)
            self.ui.draw()

            pygame.display.flip()

        pygame.quit()