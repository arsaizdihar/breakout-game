import pygame
from constant import *
import time
import random


class Brick:
    def __init__(self, x, y, total_life):
        self.x = x
        self.y = y
        self.width = BRICK_WIDTH
        self.height = BRICK_HEIGHT
        self.color = [abs(255 - x % 511), abs(255 - y % 511), 150, 255]
        self.total_life = total_life
        self.life = total_life

    def get_rect(self):
        return pygame.Rect((self.x, self.y, self.width, self.height))

    def draw(self, window):
        rect = self.get_rect()
        color = self.color.copy()
        color[1] = abs(255 - (self.color[1] + time.time()*50) % 511)
        color[3] = 255 * self.life / self.total_life
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
        window.blit(shape_surf, rect)