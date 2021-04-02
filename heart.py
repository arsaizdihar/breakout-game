import pygame
from constant import *


class Heart:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, window, image):
        window.blit(image, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def get_rect(self):
        return pygame.rect.Rect(self.x, self.y, HEART_SIZE, HEART_SIZE)

    def check_collision(self, player):
        rect = player.get_rect()
        if rect.colliderect(self.get_rect()):
            return True

    def check_out_of_window(self):
        return self.y >= HEIGHT-HEART_SIZE
