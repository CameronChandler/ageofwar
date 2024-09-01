class GameObject:
    def __init__(self):
        self.to_draw = True
        self.zorder = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, object_manager):
        ...