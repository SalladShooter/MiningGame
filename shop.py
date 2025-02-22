import pygame as pg
from spritesheet import Spritesheet
from animate import Animate
import config
from text import Text
import os

pg.font.init()

class Shop(Animate):
    def __init__(self, size_multiplier):
        self.size_multiplier = size_multiplier
        self.original_size = size_multiplier
        self.target_size = size_multiplier 
        self.size_speed = 0.75 
        self.spritesheet = Spritesheet("images/shop.png", [16, 16], [0, 0], [16 * self.size_multiplier, 16 * self.size_multiplier])
        self.open = False
        self.text_renderer = Text()
        self.upgrade_images = {}
        self.font = pg.font.Font(config.font, 24) 
        for ore in config.ores_list:
            image_path = f"images/{ore.lower()}.png"
            if os.path.exists(image_path):
                self.upgrade_images[ore] = pg.image.load(image_path)
        super().__init__(self.spritesheet)

    def draw(self, screen):
        if not self.open:
            mouse_x, mouse_y = pg.mouse.get_pos()
            shop_rect = pg.Rect(screen.get_width() // 2 - ((16 * self.size_multiplier) // 2), 8, 16 * self.size_multiplier, 16 * self.size_multiplier)

            if shop_rect.collidepoint(mouse_x, mouse_y):
                self.target_size = self.original_size * 1.1
            else:
                self.target_size = self.original_size

            self.size_multiplier += (self.target_size - self.size_multiplier) * self.size_speed
            self.spritesheet = Spritesheet("images/shop.png", [16, 16], [0, 0], [16 * self.size_multiplier, 16 * self.size_multiplier])
            super().animate(0, [0, 0], [0, 0])

        
            screen.blit(self.sprite, (screen.get_width() // 2 - ((16 * self.size_multiplier) // 2), 8))
        
        if self.open:
            overlay = pg.Surface((480, 368))
            overlay.set_alpha(255)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            mouse_x, mouse_y = pg.mouse.get_pos()

            button_size = 40
            text_size = 50

            if pg.Rect(430, 20, button_size, button_size).collidepoint(mouse_x, mouse_y):
                button_size = 40 * 1.1
                text_size = round(50 * 1.1)

            close_button_rect = pg.Rect(430 - (button_size - 40) // 2, 20 - (button_size - 40) // 2, button_size, button_size)

            pg.draw.rect(screen, (255, 25, 25), close_button_rect)

            font = pg.font.Font(config.font, text_size)
            close_text = font.render("X", True, (255, 255, 255))
            text_x = close_button_rect.x + (close_button_rect.width - close_button_rect.width // 2) // 2
            text_y = close_button_rect.y + (close_button_rect.height - close_text.get_height()) // 2
            screen.blit(close_text, (text_x, text_y))


            y_offset = 50
            for upgrade, data in config.upgrades.items():
                self.text_renderer.alpha = 255

                text_x = 50
                upgrade_text = f"{upgrade}:"
                self.text_renderer.render(
                    screen, config.font, 24, upgrade_text, True, (255, 255, 255), (text_x, y_offset)
                )

                text_surface = self.font.render(upgrade_text, True, (255, 255, 255))
                text_width = text_surface.get_width()

                icon_x = text_x + text_width + 5
                icon_y = y_offset + 7
                for ore, amount in data["cost"].items():
                    if ore in self.upgrade_images:
                        screen.blit(self.upgrade_images[ore], (icon_x, icon_y - 5))
                        amount_text = Text()
                        amount_text.alpha = 255
                        amount_text.render(screen, config.font, 20, str(amount), True, (255, 255, 255), (icon_x + 20, y_offset))
                        icon_x += 50 

                y_offset += 40

            self.close_button_rect = close_button_rect

            if not self.open:
                mouse_x, mouse_y = pg.mouse.get_pos()
                shop_rect = pg.Rect(screen.get_width() // 2 - ((16 * self.size_multiplier) // 2), 8, 16 * self.size_multiplier, 16 * self.size_multiplier)

                if shop_rect.collidepoint(mouse_x, mouse_y):
                    self.target_size = self.original_size * 1.1
                else:
                    self.target_size = self.original_size

                self.size_multiplier += (self.target_size - self.size_multiplier) * self.size_speed
                self.spritesheet = Spritesheet("images/shop.png", [16, 16], [0, 0], [16 * self.size_multiplier, 16 * self.size_multiplier])
                super().animate(0, [0, 0], [0, 0])

                screen.blit(self.sprite, (screen.get_width() // 2 - ((16 * self.size_multiplier) // 2), 8))
            
            if self.open:
                overlay = pg.Surface((480, 368))
                overlay.set_alpha(0)
                overlay.fill((0, 0, 0))
                screen.blit(overlay, (0, 0))

                y_offset = 50
                for upgrade, data in config.upgrades.items():
                    self.text_renderer.alpha = 255

                    text_x = 50
                    upgrade_text = f"{upgrade}:"
                    self.text_renderer.render(
                        screen, config.font, 24, upgrade_text, True, (255, 255, 255), (text_x, y_offset)
                    )

                    text_surface = self.font.render(upgrade_text, True, (255, 255, 255))
                    text_width = text_surface.get_width()

                    icon_x = text_x + text_width + 5
                    icon_y = y_offset + 7
                    for ore, amount in data["cost"].items():
                        if ore in self.upgrade_images:
                            screen.blit(self.upgrade_images[ore], (icon_x, icon_y - 5))
                            amount_text = Text()
                            amount_text.alpha = 255
                            amount_text.render(screen, config.font, 20, str(amount), True, (255, 255, 255), (icon_x + 20, y_offset))
                            icon_x += 50 

                    y_offset += 40

    def animate(self, from_frames=[0, 0], to_frames=[0, 0]):
        super().animate(0, from_frames, to_frames)

    def purchase(self, upgrade_name):
        global player_mining_multiplier
        upgrade = config.upgrades.get(upgrade_name)

        if upgrade:
            if all(config.ores_inventory[ore] >= amount for ore, amount in upgrade["cost"].items()):
                for ore, amount in upgrade["cost"].items():
                    config.ores_inventory[ore] -= amount
                
                player_mining_multiplier *= upgrade["multiplier"]
                print(f"Purchased {upgrade_name}! New multiplier: {player_mining_multiplier}")
                return True
            else:
                print("Not enough resources!")
                return False