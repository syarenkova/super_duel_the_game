import pygame


class Bar(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.rect = pygame.Rect(0, 0, 180, 10)
        self.rect.x = 778 if color == "red" else 30


class Health(Bar):
    def __init__(self, color):
        super().__init__(color)
        self.rect.top = 20

    def update(self, num):
        self.image = pygame.Surface((180, 10))
        pygame.draw.rect(self.image, "red", (0, 0, 18 * num, 30))


class Blocks(Bar):
    def __init__(self, color):
        super().__init__(color)
        self.rect.top = 40

    def update(self, num):
        self.image = pygame.Surface((180, 10))
        pygame.draw.rect(self.image, "yellow", (0, 0, 18 * num, 30))