import pygame as pg
from spritesheet import Spritesheet
from animate import Animate

class Pickaxe(Animate):
    def __init__(self, size_multiplier):
        self.size_multiplier = size_multiplier
        self.spritesheet = Spritesheet("images/pickaxe.png", [16, 16], [0, 0], [16 * self.size_multiplier, 16 * self.size_multiplier])
        super().__init__(self.spritesheet)

    def draw(self, screen):
        screen.blit(self.sprite, (screen.get_width() // 2 - ((16 * self.size_multiplier) // 2), screen.get_height() // 2 - ((16 * self.size_multiplier) // 2)))