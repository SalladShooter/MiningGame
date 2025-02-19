import pygame as pg
from typing import Tuple

class Animate():
    def __init__(self, spritesheet):
        self.spritesheet = spritesheet
        self.last_frame_time = pg.time.get_ticks()
        self.frame_row = 0
        self.frame_col = 0
        self.frame = [1, 1]
        self.sprite = self.spritesheet.get_sprite((self.frame_row, self.frame_col))
        
    def animate(self, frame_duration, from_frames: Tuple[int, int], to_frames: Tuple[int, int]):
        self.to_frames = [to_frames[0], to_frames[1]]
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
        if self.frame == [frames[0], frames[1]]:
            return True
        return False
