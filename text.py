import pygame as pg
from typing import Tuple

pg.font.init()

class Text:
    def __init__(self):
        self.alpha = 0
        self.fade_in = True 
        self.fade_out = False
        self.fade_timer = 0 
        self.text_visible_time = 0

    def render(self, screen, font: str, font_size: int, input_text: str, anti_aliasing: bool, color: Tuple[int,int,int], pos: Tuple[float,float]):
        self.screen = screen
        self.font = font
        self.font_size = font_size
        self.input_text = input_text
        self.anti_aliasing = anti_aliasing
        self.color = color
        self.pos = pos
        
        try:
            self.text = pg.font.Font(self.font, self.font_size)
        except FileNotFoundError:
            print(f"Error: Font file '{self.font}' not found.")
            self.text = pg.font.Font(None, self.font_size)
        
        self.text_surface = self.text.render(self.input_text, self.anti_aliasing, self.color)
        
        self.text_surface.set_alpha(self.alpha)
        
        self.screen.blit(self.text_surface, self.pos)

    def update_fade(self, fade_in_speed: int, fade_out_speed: int, hold_duration: int, item_added: bool):
        if self.fade_in:
            if self.alpha < 255:
                self.alpha += fade_in_speed
                if self.alpha > 255:
                    self.alpha = 255

            if self.alpha == 255:
                self.text_visible_time += 1
                if self.text_visible_time >= hold_duration:
                    self.fade_in = False
                    self.fade_out = True
                    self.text_visible_time = 0

        if self.fade_out:
            if self.alpha > 0:
                self.alpha -= fade_out_speed
                if self.alpha < 0:
                    self.alpha = 0

            if self.alpha == 0:
                self.fade_out = False
                self.text_visible_time = 0
                if item_added:
                    self.fade_in = True
