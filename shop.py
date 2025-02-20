import pygame as pg
from spritesheet import Spritesheet
from animate import Animate

class Shop(Animate):
    def __init__(self, size_multiplier):
        self.size_multiplier = size_multiplier
        self.original_size = size_multiplier
        self.target_size = size_multiplier 
        self.size_speed = 0.75 
        self.spritesheet = Spritesheet("images/shop.png", [16, 16], [0, 0], [16 * self.size_multiplier, 16 * self.size_multiplier])
        super().__init__(self.spritesheet)

    def draw(self, screen, size_multiplier):
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

    def animate(self, from_frames = [0, 0], to_frames = [0, 0]):
        super().animate(0, from_frames, to_frames)
