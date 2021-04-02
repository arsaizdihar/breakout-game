from constant import *
import pygame
import time
import random
from heart import Heart


class Paddle:
    def __init__(self, x, y):
        self.init_x = x
        self.init_y = y
        self.x = x
        self.y = y
        self.width = PADDLE_WIDTH
        self.height = SIZE
        self.bullets = []
        self.shoot_cooldown = 0

    def get_rect(self):
        return pygame.Rect((self.x, self.y, self.width, self.height))

    def draw(self, window):
        def get_pos_color(adj):
            return abs(255 - (self.x + adj) % 511)
        color = (255, 50, get_pos_color(time.time()*255))
        pygame.draw.rect(window, color, self.get_rect())

    def right(self, vel):
        self.x += vel
        if self.get_rect().right > WIDTH:
            self.x -= vel

    def left(self, vel):
        self.x -= vel
        if self.get_rect().left < 0:
            self.x += vel

    def reset(self):
        self.x = self.init_x
        self.y = self.init_y

    def shoot(self, sound):
        if self.shoot_cooldown <= 0:
            sound.play()
            self.shoot_cooldown = SHOOT_COOLDOWN
            self.bullets.append(Bullet(self.get_rect().centerx - SIZE / 2, self.y - SIZE))


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_rect(self):
        return pygame.Rect((self.x, self.y, SIZE, SIZE))

    def draw(self, window, vel):
        self.y -= vel
        pygame.draw.rect(window, 'yellow', self.get_rect())

    def check_out_of_window(self):
        return self.y <= SCOREBOARD_HEIGHT

    def check_brick_collision(self, bricks, hearts):
        rect = self.get_rect()
        for brick in bricks:
            if rect.colliderect(brick.get_rect()):
                brick.life -= 1
                if brick.life == 0:
                    if random.random() >= 0.95:
                        hearts.append(Heart(brick.get_rect().centerx - HEART_SIZE / 2, brick.y + brick.height))
                    bricks.remove(brick)
                return True
