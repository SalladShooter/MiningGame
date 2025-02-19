import pygame as pg
import time
from pickaxe import Pickaxe

pg.init()
screen = pg.display.set_mode((480, 368))
pg.display.set_caption('Rougelite Game')
clock = pg.time.Clock()
running = True

frame_duration = 50

pickaxe = Pickaxe()

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
    elif]:
        pickaxe.animate(frame_duration, [0, 0], [0, 0])
    
    pickaxe.draw(screen)

    pg.display.flip()

    clock.tick(60)

pg.quit()
