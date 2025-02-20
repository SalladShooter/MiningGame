import pygame as pg
from spritesheet import Spritesheet
from animate import Animate

class TaxMaster(Animate):
    def __init__(self, size_multiplier):
        self.size_multiplier = size_multiplier
        self.spritesheet = Spritesheet("images/tax_master.png", [16, 32], [0, 0], [16 * self.size_multiplier, 32 * self.size_multiplier])
        super().__init__(self.spritesheet)

    def draw(self, screen):
        screen.blit(self.sprite, (screen.get_width() - ((16 * self.size_multiplier)), 0))