class GameObject:
    def __init__(self):
        self.to_draw = True

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, game, delta):
        ...