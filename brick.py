import pygame
from constant import *
import time


class Brick:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = BRICK_WIDTH
        self.height = BRICK_HEIGHT
        self.color = [abs(255 - x % 511), abs(255 - y % 511), 150]

    def get_rect(self):
        return pygame.Rect((self.x, self.y, self.width, self.height))

    def draw(self, window):
        color = self.color.copy()
        color[1] = abs(255 - (self.color[1] + time.time()*50) % 511)
        pygame.draw.rect(window, color, self.get_rect())
