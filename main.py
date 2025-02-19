import pygame as pg
import time
from pickaxe import Pickaxe
from rock import Rock
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

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill("black")
    
    mouse_buttons = pg.mouse.get_pressed()
    
    if mouse_buttons[0]:
        canAnimate = True
    if canAnimate:
        pickaxe.animate(frame_duration, [0, 0], [2, 2])
        if pickaxe.check_frame([2, 2]):
            canAnimate = False
            rock.animate(frame_duration * 4, [0, 0], [3, 1])
    else:
        pickaxe.animate(frame_duration, [0, 0], [0, 0])
    
    rock.draw(screen)
    pickaxe.draw(screen)

    pg.display.flip()

    clock.tick(60)

pg.quit()
