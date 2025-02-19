import pygame as pg
from spritesheet import Spritesheet
from typing import Tuple

class Pickaxe:
    def __init__(self):
        self.last_frame_time = pg.time.get_ticks()
        self.spritesheet = Spritesheet("images/pickaxe.png", [16, 16], [0, 0], [64, 64])
        self.frame_row = 0
        self.frame_col = 0
        self.frame = [1, 1]
        self.sprite = self.spritesheet.get_sprite((self.frame_row, self.frame_col))

    def animate(self, frame_duration, from_frames: Tuple[int, int], to_frames: Tuple[int, int]):
        self.to_frames = [to_frames[0]+1,to_frames[1]+1]
        self.from_frames = from_frames
        self.frame_row = self.frame_row + self.from_frames[0] 
        self.frame_col = self.frame_col + self.from_frames[1]
        
        self.frame_duration = frame_duration
        self.current_time = pg.time.get_ticks()

        if self.current_time - self.last_frame_time > self.frame_duration:
            
            self.frame_col += 1

            if self.frame_col >= self.to_frames[0]:
                self.frame_col = 0
                self.frame_row += 1
                
                if self.frame_row >= self.to_frames[1]:
                    self.frame_row = self.from_frames[0]

            self.last_frame_time = self.current_time

        self.sprite = self.spritesheet.get_sprite((self.frame_row, self.frame_col))
        self.frame = [self.frame_col, self.frame_row]
    
    def check_frame(self, frames: Tuple[int, int]):
        if self.frame == [frames[0]-1, frames[1]-1]:
            return True
        return False

    def draw(self, screen):
        screen.blit(self.sprite, (50, 50))
