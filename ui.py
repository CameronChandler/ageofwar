import pygame
from constants import Color, BoxAction, P1_KEYS, P2_KEYS, CONFIG_NAME
import json

with open(CONFIG_NAME, 'r') as file:
    config = json.load(file)

EVOLUTION_COST = {evolution: cost for evolution, cost in enumerate(config['evolution_costs'])}


class MinionBox:
    size = 70
    text_box_size = 30
    padding = 20
    line_width = 4

    def __init__(self, x, y, player: int):
        self.x = x
        self.y = y
        self.player = player
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.selected = False
        self.box_color = Color.GREY

    def draw_box(self, screen):
        pygame.draw.rect(screen, self.box_color, self.rect, self.line_width)

        y = self.y - self.text_box_size + self.line_width
        pygame.draw.rect(screen, self.box_color, (self.x, y, self.size, self.text_box_size), self.line_width)

    def draw_minion(self, screen, MinionClass):
        image = pygame.image.load(MinionClass.image_path)
        rect = image.get_rect(topleft=(0, 0))
        original_length = max(rect.width, rect.height)
        new_size = (
            (0.8 * self.size * rect.width ) // original_length,
            (0.8 * self.size * rect.height) // original_length
        )

        image = pygame.transform.scale(image, new_size)
        image_x = self.x + (self.size - new_size[0]) // 2
        image_y = self.y + (self.size - new_size[1]) // 2
        screen.blit(image, (image_x, image_y))

    def draw_price(self, screen, cost: int, color):
        font = pygame.font.Font(None, 24)

        text = font.render(f'${cost}', True, color)
        rect = text.get_rect(center=(self.x + self.size/2, self.y - self.text_box_size/2 + self.line_width))
        screen.blit(text, rect)

    def draw(self, screen, base, MinionClass):
        self.draw_box(screen)
        self.draw_minion(screen, MinionClass)
        color = Color.YELLOW if base.budget >= MinionClass.cost else Color.GREY
        self.draw_price(screen, MinionClass.cost, color)

class ActionBox:
    size = 80
    padding = 30
    line_width = 4
    
    def __init__(self, x, y, action, player):
        self.x = x
        self.y = y
        self.action = action
        self.player = player
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.selected = False

    def get_font_color(self, base):
        if self.action == BoxAction.EVOLVE:
            return Color.YELLOW if base.can_evolve else Color.WHITE
        if self.action == BoxAction.TURRET_1:
            return Color.YELLOW if base.can_upgrade_turret(1) else Color.WHITE
        if self.action == BoxAction.TURRET_2:
            return Color.YELLOW if base.can_upgrade_turret(2) else Color.WHITE
        return Color.WHITE
    
    def get_text(self, base) -> str:
        text = self.action
        if self.action == BoxAction.EVOLVE:
            if base.evolution in EVOLUTION_COST:
                text += f'\n{EVOLUTION_COST[base.evolution]}xp'
            else:
                text = 'Fully\nEvolved'
        elif self.action in (BoxAction.TURRET_1, BoxAction.TURRET_2):
            text += f'\n${base.turret_choice.cost}'
        return text

    def draw(self, screen, base):
        color = Color.YELLOW if self.selected else Color.GREY
        pygame.draw.rect(screen, color, self.rect, self.line_width)
        font = pygame.font.Font(None, 24)
        lines = self.get_text(base).split('\n')

        y_offset = 20
        for i, line in enumerate(lines):
            action_text = font.render(line, True, self.get_font_color(base))
            y_pos = self.rect.centery
            if self.action != BoxAction.POWER:
                y_pos += i*y_offset - y_offset/3
            action_rect = action_text.get_rect(center=(self.rect.centerx, y_pos))
            screen.blit(action_text, action_rect)

class UI:

    def __init__(self, bases, screen, screen_width, screen_height):
        self.bases = bases
        self.screen = screen
        self.screen_width  = screen_width
        self.screen_height = screen_height

        self.font = pygame.font.Font(None, 36)

        self.initialise_action_boxes()
        self.initialise_minion_boxes()

    def initialise_action_boxes(self):
        x1, x2 = ActionBox.padding, 2*ActionBox.padding + ActionBox.size
        y1 = 100
        y2 = y1 + ActionBox.padding + ActionBox.size
        self.action_boxes_p1 = [
            [ActionBox(x1, y1, BoxAction.EVOLVE, player=1),  ActionBox(x2, y1, BoxAction.TURRET_1, player=1)],
            [ActionBox(x1, y2, BoxAction.POWER , player=1),  ActionBox(x2, y2, BoxAction.TURRET_2, player=1)]
        ]
        x1 = self.screen_width - 2*(ActionBox.padding + ActionBox.size)
        x2 = self.screen_width - ActionBox.padding - ActionBox.size
        self.action_boxes_p2 = [
            [ActionBox(x1, y1, BoxAction.EVOLVE, player=2), ActionBox(x2, y1, BoxAction.TURRET_1, player=2)],
            [ActionBox(x1, y2, BoxAction.POWER , player=2), ActionBox(x2, y2, BoxAction.TURRET_2, player=2)]
        ]

        self.selected_box_p1 = (0, 0)
        self.selected_box_p2 = (0, 0)

    def initialise_minion_boxes(self):
        num_minion_choices = len(self.bases[1].minion_choices)
        x = 380
        y = 40

        unit_width = MinionBox.size + MinionBox.padding
        xs = [x + i*unit_width for i in range(num_minion_choices)]
        self.minion_boxes_p1 = [MinionBox(xs[i], y, player=1) for i in range(num_minion_choices)]

        xs = [self.screen_width - x - (num_minion_choices - 2 + i)*unit_width for i in range(num_minion_choices)]
        self.minion_boxes_p2 = [MinionBox(xs[i], y, player=2) for i in range(num_minion_choices)]

    def draw_action_boxes(self):
        for row in self.action_boxes_p1 + self.action_boxes_p2:
            for box in row:
                box.draw(self.screen, self.bases[box.player])

    def draw_minion_boxes(self):
        minion_boxes = self.minion_boxes_p1 + self.minion_boxes_p2
        minion_choices = (
            list(self.bases[1].minion_choices.values()) + 
            list(self.bases[2].minion_choices.values())
        )
        for box, MinonClass in zip(minion_boxes, minion_choices):
            box.draw(self.screen, self.bases[box.player], MinonClass)

    def update_selection(self, pressed_keys, keys, selected_box):
        row, col = selected_box
        if keys['up'] in pressed_keys:    row = max(0, row - 1)
        if keys['down'] in pressed_keys:  row = min(1, row + 1)
        if keys['left'] in pressed_keys:  col = max(0, col - 1)
        if keys['right'] in pressed_keys: col = min(1, col + 1)
        return (row, col)

    def update(self, pressed_keys) -> list[tuple[int, BoxAction]]:
        ''' Takes pressed keys and returns list of player ui selections '''
        self.selected_box_p1 = self.update_selection(pressed_keys, P1_KEYS, self.selected_box_p1)
        self.selected_box_p2 = self.update_selection(pressed_keys, P2_KEYS, self.selected_box_p2)

        # Update box highlighting
        for i, row in enumerate(self.action_boxes_p1):
            for j, box in enumerate(row):
                box.selected = (i, j) == self.selected_box_p1

        for i, row in enumerate(self.action_boxes_p2):
            for j, box in enumerate(row):
                box.selected = (i, j) == self.selected_box_p2

        ui_selections = []
        # If players make selection
        if pygame.K_SPACE in pressed_keys:
            row, col = self.selected_box_p1
            box = self.action_boxes_p1[row][col]
            ui_selections.append((box.player, box.action))

        if pygame.K_RETURN in pressed_keys:
            row, col = self.selected_box_p2
            box = self.action_boxes_p2[row][col]
            ui_selections.append((box.player, box.action))

        return ui_selections

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
        num_squares = self.bases[1].max_queue_length
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
        self.draw_minion_boxes()
        self.draw_training_queues()
        self.draw_action_boxes()