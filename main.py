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
inventory = config.ores_inventory
text = Text()
font_size = 30

shop_text = Text()
close_text = Text()

items_text = []
for i in range(len(config.ores_list)):
    items_text.append(Text())
    
ore_images = {}
for ore in config.ores_list:
    image_path = f"images/{ore.lower()}.png"
    if os.path.exists(image_path):
        ore_images[ore] = pg.image.load(image_path)
    else:
        print(f"Warning: Image {image_path} not found.")

item_added = False
fade_in = False
fade_out = False
fade_in_duration = 1
fade_out_duration = 100
hold_duration = 50

fade_timer = 0
wiggle_frame = 0

shop_open = False

last_mined_ore = None

clear()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()
            if not shop.open:
                shop_rect = pg.Rect(screen.get_width() // 2 - ((16 * shop.size_multiplier) // 2), 8, 16 * shop.size_multiplier, 16 * shop.size_multiplier)
            if shop.open and shop.close_button_rect.collidepoint(mouse_x, mouse_y):
                shop_open = not shop_open
                shop.open = shop_open
            else:
                shop_rect = pg.Rect(screen.get_width() // 2 - ((16 * shop.size_multiplier) // 2), 8, 16 * shop.size_multiplier, 16 * shop.size_multiplier)
                if shop_rect.collidepoint(mouse_x, mouse_y):
                    shop_open = not shop_open
                    shop.open = shop_open
                    upgrade_list = list(config.upgrades)
                    for i, upgrade in enumerate(upgrade_list):
                        if 50 <= mouse_x <= 300 and 50 + (i * 30) <= mouse_y <= 80 + (i * 30):
                            shop.purchase(upgrade)

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
                mined_ore = config.ores_list[rand.randint(0, len(config.ores_list) - 1)]
                config.ores_inventory[mined_ore] += int(config.player_mining_multiplier)
                last_mined_ore = mined_ore
                inventory = config.ores_inventory
                rock.reset_wiggle()
                item_added = True
                fade_in = True
                fade_out = False
    else:
        pickaxe.animate(frame_duration, [0, 0], [0, 0])

    shop.animate()
    shop.draw(screen)
    
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

    if last_mined_ore:
        text.render(screen, config.font, font_size, f"+1 {last_mined_ore}", True, [226, 243, 228], [16, 8])
        
    for i in range (len(config.ores_list)):
        items_text[i].alpha = 255
        inventory_item = inventory[config.ores_list[i]]
        text_x = 16
        image_x = text_x + (len(str(inventory_item)) * 16) - 4 // 1.5
        image_y = (16*size_multiplier) + (i*18) 

        items_text[i].render(screen, config.font, font_size, f"{inventory_item}", True, [226, 243, 228], [text_x, image_y - 8])
        
        if config.ores_list[i] in ore_images:
            screen.blit(ore_images[config.ores_list[i]], (image_x, image_y))


    if shop_open:
        shop.draw(screen)

    pg.display.flip()
    clock.tick(60)
