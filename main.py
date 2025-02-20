import pygame as pg
import time
from pickaxe import Pickaxe
from rock import Rock
from text import Text
from shop import Shop
from tax_master import TaxMaster
import config
import random as rand
import os

def clear():
    os.system('cls' if os.name=='nt' else 'clear')

pg.init()
screen = pg.display.set_mode((480, 368))
pg.display.set_caption('Mining Game')
clock = pg.time.Clock()
running = True

frame_duration = 50
size_multiplier = 4

pickaxe = Pickaxe(size_multiplier)
rock = Rock(size_multiplier)
shop = Shop(size_multiplier)
tax_master = TaxMaster(size_multiplier)

canAnimate = False
inventory = ['']
text = Text()
font_size = 30

shop_text = Text()
close_text = Text()

item_added = False
fade_in = False
fade_out = False
fade_in_duration = 1
fade_out_duration = 100
hold_duration = 50

fade_timer = 0
wiggle_frame = 0

shop_open = False

clear()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()
            shop_rect = pg.Rect(screen.get_width() // 2 - ((16 * shop.size_multiplier) // 2), 8, 16 * shop.size_multiplier, 16 * shop.size_multiplier)
            if shop_rect.collidepoint(mouse_x, mouse_y):
                shop_open = not shop_open
            elif shop_open:
                shop_open = False

    screen.fill("black")
    
    mouse_buttons = pg.mouse.get_pressed()
    
    if mouse_buttons[0] and not shop_open:
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

    shop.animate()
    shop.draw(screen, size_multiplier)
    
    tax_master.animate(frame_duration * 2.25, [0, 0], [2, 2])
    tax_master.draw(screen)
    
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
        text.render(screen, config.font, font_size, f"+1 {inventory[len(inventory) - 1]}", True, [226, 243, 228], [16, 8])

    if shop_open:
        overlay = pg.Surface((480, 368))
        overlay.set_alpha(255)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        shop_text.alpha = 255
        shop_font = "Shop Menu"
        shop_text.render(screen, config.font, font_size, shop_font, True, [226, 243, 228], [screen.get_width() // 2 - 7*len(shop_font),  16])

        close_text.alpha = 200
        close_font = "Click Anywhere To Close"
        close_text.render(screen, config.font, font_size, close_font, True, [226, 243, 228], [screen.get_width() // 2 - 7*len(close_font), screen.get_height() // 2])


    pg.display.flip()
    clock.tick(60)
