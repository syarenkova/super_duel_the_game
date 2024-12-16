import pygame
import time
import random
from bullet import Bullet

WIN_WIDTH = 988

boxes = [pygame.image.load("gun_with_blocks/ghost_box.png"),
         pygame.transform.scale(pygame.image.load("gun_with_blocks/tourel_box.png"), (23, 23)),
         pygame.image.load("gun_with_blocks/gun_box.png"),
         pygame.image.load("gun_with_blocks/bullet_box.png")]


def opponent_color(color):
    return "red" if color == "blue" else "blue"


def load_image(name, colorkey=None):
    fullname = name
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if colorkey == -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
    return image


class Gun(pygame.sprite.Sprite):
    bullets = pygame.sprite.Group()

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("gun_with_blocks/gun.png")
        self.rect = self.image.get_rect().move(x, y)
        self.destination = 1
        self.next_box_time()

    def update(self, platforms):
        self.rect.x += self.destination
        if self.rect.left <= 0 or self.rect.right >= WIN_WIDTH:
            self.destination *= -1

    def check_box(self):
        if time.time() > self.next_box:
            self.next_box_time()
            return Box(self.rect.x, self.rect.y)

    def next_box_time(self):
        self.next_box = time.time() + (1 + random.random()) * 5

    def crashed_block(self):
        if c := self.bullets.sprites():
            return c[0].return_crashed_blocks()
        return []


class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        num = random.randint(0, 3)
        self.image = boxes[num]
        self.type = drops[num]
        self.rect = self.image.get_rect().move(x, y)
        self.destination = 8

    def make_drop(self, hero):
        self.kill()
        return self.type(hero)

    def update(self, platforms):
        self.rect.y += self.destination
        if pygame.sprite.spritecollideany(self, platforms):
            self.destination = 0
            self.rect.y -= 1


class Ghost(pygame.sprite.Sprite):
    image = pygame.image.load("gun_with_blocks/ghost.png")

    def __init__(self, hero):
        super().__init__()
        self.color = opponent_color(hero.color)
        self.rect = self.image.get_rect().move(500, -100)

    def update(self, heroes):
        hero = tuple(filter(lambda x: x.color == self.color, heroes.sprites()))[0]
        x, y = hero.rect.x, hero.rect.y
        x_s, y_s = self.rect.x, self.rect.y
        s = ((x_s - x) ** 2 + (y_s - y) ** 2) ** 0.5 // 1
        x_to = (x - x_s) / (s / 2) // 1
        y_to = (y - y_s) / (s / 2) // 1
        self.rect = self.rect.move(x_to, y_to)
        if hero := pygame.sprite.spritecollideany(self, heroes):
            hero.health -= 2
            self.kill()


class Tourell(pygame.sprite.Sprite):
    blue = pygame.transform.scale(pygame.image.load("gun_with_blocks/tourel.png"), (114, 78))
    red = pygame.transform.scale(load_image("gun_with_blocks/tourel_2.png"), (114, 78))
    bullet = pygame.transform.scale(pygame.image.load("gun_with_blocks/bullet.png"), (23, 20))

    def __init__(self, hero):
        super().__init__()
        self.image = self.blue if hero.color == "blue" else self.red
        self.drone = self.image
        self.color = opponent_color(hero.color)
        self.rect = self.image.get_rect().move(500, -100)
        self.health = 3
        self.image.blit(self.bullet, (39, 50))
        self.next_box = time.time() + (1 + random.random()) * 5
        #self.rect = self.image.get_rect().move(x, y)

    def update(self, heroes):
        hero = tuple(filter(lambda x: x.color == self.color, heroes.sprites()))[0]
        x, y = hero.rect.x, hero.rect.y
        x_s, y_s = self.rect.x, self.rect.y
        s = ((x_s - x) ** 2 + (y_s - y) ** 2 + 40000) ** 0.5 // 1
        x_to = (x - x_s) / (s / 2) // 1
        y_to = (y - y_s) / (s / 2) // 1
        self.rect = self.rect.move(x_to, y_to)
        if time.time() > self.next_box:
            self.next_box = time.time() + (1 + random.random()) * 5
            Gun.bullets.add(Bullet(self.rect.x, self.rect.y, x, y))


class Adding(pygame.sprite.Sprite):
    image = pygame.Surface((20, 20))
    rect = pygame.Rect(0, 0, 20, 20)

    def __init__(self, hero):
        super().__init__()
        hero.blocks_and_bullets += 5
        self.kill()


class Bullet_box(pygame.sprite.Sprite):
    image = pygame.Surface((20, 20))
    rect = pygame.Rect(0, 0, 20, 20)

    def __init__(self, hero):
        super().__init__()
        self.color = hero.color

    def update(self, heroes):
        hero = tuple(filter(lambda x: x.color == self.color, heroes.sprites()))[0]
        hero_2 = tuple(filter(lambda x: x.color != self.color, heroes.sprites()))[0]
        Gun.bullets.add(Bullet(hero.rect.x, hero.rect.y, hero_2.rect.x, hero_2.rect.y, color=hero.color))
        self.kill()


drops = [Ghost, Tourell, Adding, Bullet_box]
