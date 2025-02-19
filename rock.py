import pygame as pg
from spritesheet import Spritesheet
from typing import Tuple
from animate import Animate
import random as rand

class Rock(Animate):
    def __init__(self, size_multiplier):
        self.size_multiplier = size_multiplier
        self.spritesheet = Spritesheet("images/mining_rock.png", [16, 16], [0, 0], [16 * self.size_multiplier, 16 * self.size_multiplier])
        super().__init__(self.spritesheet)

        self.wiggle_offset = [0, 0]

    def wiggle(self):
        self.wiggle_offset = [rand.randint(int(self.size_multiplier), int(self.size_multiplier)), 0]

    def reset_wiggle(self):
        self.wiggle_offset = [0, 0]

    def draw(self, screen):
        x_position = screen.get_width() // 2 - ((16 * self.size_multiplier) // 2) + (16 * self.size_multiplier // 2 - 8) + self.wiggle_offset[0]
        y_position = screen.get_height() // 2 - ((16 * self.size_multiplier) // 2) + (16 * self.size_multiplier // 2 - 8) + self.wiggle_offset[1]

        screen.blit(self.sprite, (x_position, y_position))

    def animate(self, frame_duration, *args):
        super().animate(frame_duration, *args)
