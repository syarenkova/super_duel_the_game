import sys

import pygame.sprite

from player import *
from blocks import *
from gun import *

WIN_WIDTH = 988
WIN_HEIGHT = 598
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_IMAGE = pygame.image.load('background-color/background_color_1.jpg')

level = [
    "-                                    -",
    "-                                    -",
    "-                                    -",
    "-                                    -",
    "-----                            -----",
    "---     *                    *     ---",
    "--    ---                    ---    --",
    "-      --                    --      -",
    "-       -                    -       -",
    "-       ---                ---       -",
    "--   -----                  -----   --",
    "-       -                    -       -",
    "-       *                    *       -",
    "-      --                    --      -",
    "---     -                    -     ---",
    "--      *                    *      --",
    "-     ----                  ----     -",
    "-        -                  -        -",
    "-----    *                  *    -----",
    "-       --                  --       -",
    "-                                    -",
    "-                                    -",
    "--------------------------------------",
    "--------------------------------------"]


def make_level():
    global level, platforms, entities, hero, hero_2, gun
    entities = pygame.sprite.Group()
    entities.add(hero)
    entities.add(hero_2)
    entities.add(gun)
    platforms = pygame.sprite.Group()
    x = y = 0
    for row in level:
        for col in row:
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.add(pf)
            if col == "*":
                bd = BlockDie(x, y)
                entities.add(bd)
                platforms.add(bd)

            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if colorkey == -1:
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    image = image.convert_alpha()
    return image


def start_screen():
    global level
    intro_text = ["Чтобы выбрать уровень введите", "число на клавиатуре от 1 до 6"]

    fon = pygame.transform.scale(BACKGROUND_IMAGE, (WIN_WIDTH, WIN_HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 36)
    text_coord = 250
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 300
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    hero = pygame.transform.scale(pygame.image.load("players/0.png"), (110, 165))
    screen.blit(hero, (325, 50))
    hero = pygame.transform.scale(pygame.image.load("players/0_2.png"), (110, 165))
    screen.blit(hero, (525, 50))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if 1073741914 <= event.key < 1073741918:
                    with open(f"levels/{(event.key - 2) % 6}.txt") as lvl:
                        level = [line.strip() for line in lvl.readlines()]
                elif event.key == 1073741918:
                    with open("levels/6.txt") as lvl:
                        level = [line.strip() for line in lvl.readlines()]
                return True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(60)


def finish_screen(color):
    global level
    intro_text = [f"Выиграл {'синий' if color == 'blue' else 'красный'}!", "", "Чтобы выбрать уровень введите",
                  "число на клавиатуре от 1 до 6"]

    fon = pygame.transform.scale(BACKGROUND_IMAGE, (WIN_WIDTH, WIN_HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 36)
    text_coord = 250
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 500 - intro_rect.width // 2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    hero = pygame.transform.scale(pygame.image.load(f"players/{'j' if color == 'blue' else 'j2'}.png"), (110, 165))
    screen.blit(hero, (445, 50))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if 1073741914 <= event.key < 1073741918:
                    with open(f"levels/{(event.key - 2) % 6}.txt") as lvl:
                        level = [line.strip() for line in lvl.readlines()]
                elif event.key == 1073741918:
                    with open("levels/6.txt") as lvl:
                        level = [line.strip() for line in lvl.readlines()]
                return True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(60)


def main():
    global level, entities, platforms, hero, hero_2, gun

    hero_2 = Player(155, 514)
    hero = Player(WIN_WIDTH - 180, 514, red=1)
    heroes = pygame.sprite.Group()
    heroes.add(hero, hero_2)

    gun = Gun(400, 5)

    all_boxes = pygame.sprite.Group()
    entities = pygame.sprite.Group()
    all_drops = pygame.sprite.Group()

    entities.add(hero)
    entities.add(hero_2)
    entities.add(hero.bar)
    entities.add(hero_2.bar)
    entities.add(gun)

    make_level()

    running = True

    while running:
        for e in pygame.event.get():
            if e.type == QUIT:
                running = False
            elif e.type == KEYDOWN:
                if e.key == K_w:
                    hero_2.up = True
                elif e.key == K_a:
                    hero_2.left = True
                elif e.key == K_d:
                    hero_2.right = True
                elif e.key == K_s:
                    new_l = list(map(list, level))
                    if new_l[hero_2.rect.y // 26 + 2][hero_2.rect.x // 26] == " " and hero_2.blocks_and_bullets > 0:
                        new_l[hero_2.rect.y // 26 + 2][hero_2.rect.x // 26] = "-"
                        hero_2.blocks_and_bullets -= 1
                        level = list(map("".join, new_l))
                        make_level()
                elif e.key == K_UP:
                    hero.up = True
                elif e.key == K_LEFT:
                    hero.left = True
                elif e.key == K_RIGHT:
                    hero.right = True
                elif e.key == K_DOWN:
                    new_l = list(map(list, level))
                    try:
                        if new_l[hero.rect.y // 26 + 2][hero.rect.x // 26] == " " and hero.blocks_and_bullets > 0:
                            new_l[hero.rect.y // 26 + 2][hero.rect.x // 26] = "-"
                            hero.blocks_and_bullets -= 1
                            level = list(map("".join, new_l))
                            make_level()
                    except:
                        pass

            elif e.type == KEYUP:
                if e.key == K_w:
                    hero_2.up = False
                elif e.key == K_d:
                    hero_2.right = False
                elif e.key == K_a:
                    hero_2.left = False
                elif e.key == K_UP:
                    hero.up = False
                elif e.key == K_RIGHT:
                    hero.right = False
                elif e.key == K_LEFT:
                    hero.left = False

        if col := pygame.sprite.spritecollideany(hero, all_boxes):
            all_drops.add(col.make_drop(hero))

        if col := pygame.sprite.spritecollideany(hero_2, all_boxes):
            all_drops.add(col.make_drop(hero_2))

        screen.blit(BACKGROUND_IMAGE, (0, 0))
        gun.update(platforms.sprites())
        box = gun.check_box()
        if box:
            all_boxes.add(box)
        hero.update(platforms.sprites())
        hero_2.update(platforms.sprites())
        all_boxes.draw(screen)
        all_boxes.update(platforms.sprites())
        platforms.update()

        all_drops.draw(screen)
        try:
            all_drops.update(heroes)
            heroes.sprites()[1]
        except:
            print(f"Выиграл {heroes.sprites()[0].color}")
            return heroes.sprites()[0].color
        entities.draw(screen)
        for h in [hero, hero_2]:
            for bar in h.bar.sprites():
                screen.blit(bar.image, (bar.rect.x, bar.rect.y))

        gun.bullets.update(heroes, platforms)
        gun.bullets.draw(screen)
        for pos in gun.crashed_block():
            new_l = list(map(list, level))
            new_l[pos[0]][pos[1]] = " "
            level = list(map("".join, new_l))

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Super Duel - The Game")
    clock = pygame.time.Clock()

    start_screen()
    while True:
        if color := main():
            if not finish_screen(color):
                break
        else:
            break
    terminate()
