import pygame

PLATFORM_WIDTH = 26
PLATFORM_HEIGHT = 26


class Platform(pygame.sprite.Sprite):
    image = pygame.image.load("blocks/platform1.png")

    def __init__(self, x, y):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.health = 3
        self.rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

    def update(self):
        if self.health <= 0:
            self.kill()


class BlockDie(Platform):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("blocks/gun.png")