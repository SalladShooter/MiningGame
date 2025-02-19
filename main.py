import pygame as pg
import time
from pickaxe import Pickaxe
from rock import Rock
from text import Text
import config
import random as rand

pg.init()
screen = pg.display.set_mode((480, 368))
pg.display.set_caption('Mining Game')
clock = pg.time.Clock()
running = True

frame_duration = 50
size_multiplier = 4

pickaxe = Pickaxe(size_multiplier)
rock = Rock(size_multiplier)

canAnimate = False

inventory = ['']

text = Text()

font_size = 30

item_added = False

fade_in = False
fade_out = False
fade_in_duration = 1
fade_out_duration = 100
hold_duration = 50

fade_timer = 0

wiggle_frame = 0

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill("black")
    
    mouse_buttons = pg.mouse.get_pressed()
    
    if mouse_buttons[0]:
        canAnimate = True
    if canAnimate:
        pickaxe.animate(frame_duration, [0, 0], [3, 3])
        if pickaxe.check_frame([2, 2]):
            canAnimate = False
            rock.animate(frame_duration, [0, 0], [4, 2])
            if wiggle_frame < 1:
                rock.wiggle()
                wiggle_frame += 1
            else:
                rock.reset_wiggle()
                wiggle_frame = 0
            if rock.check_frame([3, 1]) and not item_added:
                inventory.append(config.ores[rand.randint(0, len(config.ores) - 1)])
                rock.reset_wiggle()
                item_added = True
                fade_in = True
                fade_out = False

    else:
        pickaxe.animate(frame_duration, [0, 0], [0, 0])

    rock.draw(screen)
    pickaxe.draw(screen)
    
    if item_added and fade_in:
        fade_timer += 1
        if fade_timer <= fade_in_duration:
            text.update_fade(255, 0, hold_duration, item_added)
        else:
            fade_timer = 0
            fade_in = False
            fade_out = True

    if fade_out:
        fade_timer += 1
        if fade_timer <= fade_out_duration:
            text.update_fade(0, 10, hold_duration, item_added)
        else:
            fade_timer = 0
            fade_out = False
            if item_added:
                item_added = False
                fade_in = True

    if inventory[len(inventory) - 1] != "":
        text.render(screen, config.font, font_size, f"+1 {inventory[len(inventory) - 1]}", True, [255, 255, 255], [16, 8])

    pg.display.flip()

    clock.tick(60)
