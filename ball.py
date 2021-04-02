import pygame

from constant import *
import math
import random

from paddle import Paddle


class Ball:
    def __init__(self, x, y):
        self.init_x = x
        self.init_y = y
        self.x = x
        self.y = y
        self.angle = random.randint(60, 120)
        self.vel_x = 0
        self.vel_y = 0
        self.vel = 0
        self.circle = None
        self.cooldown_time = 0

    def move(self, vel, dt, sound):
        if self.cooldown_time <= 0:
            self.vel = vel
            self.vel_x = vel * math.cos(-self.angle / 180 * math.pi)
            self.vel_y = vel * math.sin(-self.angle / 180 * math.pi)
            self.x += self.vel_x
            self.y += self.vel_y
            if self.x < 0:
                self.x = 0
                self.angle = 180 - self.angle
                sound.play()
            elif self.x > WIDTH-SIZE:
                self.x = WIDTH-SIZE
                self.angle = 180 - self.angle
                sound.play()
            elif self.y < SCOREBOARD_HEIGHT:
                self.y = SCOREBOARD_HEIGHT
                self.angle = 360 - self.angle
                sound.play()
            self.angle = (self.angle + 360) % 360
        else:
            self.cooldown_time -= dt*16

    def draw(self, window):
        self.circle = pygame.draw.circle(window, 'white', (self.x + SIZE / 2, self.y + SIZE / 2), SIZE/2)

    def player_collision(self, player: Paddle):
        if self.circle:
            rect = player.get_rect()
            player_left = rect.left
            if rect.colliderect(self.circle) and self.circle.top-self.vel_y <= rect.top:
                self.y = rect.top - SIZE
                self.angle = 30 + (1-(self.circle.centerx - player_left)/player.width)*120
                if self.angle < 30:
                    self.angle = 30
                elif self.angle > 150:
                    self.angle = 150
                return True

    def brick_collision(self, bricks):
        if self.circle:
            circle_centerx = self.circle.centerx
            for brick in bricks:
                rect = brick.get_rect()
                if rect.colliderect(self.circle):
                    if rect.left-SIZE/2+self.vel < circle_centerx < rect.right+SIZE/2-self.vel:
                        self.angle = 360 - self.angle
                    else:
                        self.angle = 180 - self.angle
                    self.angle = (self.angle + 360) % 360
                    bricks.remove(brick)
                    return True

    def check_dead(self):
        return self.y > HEIGHT-SIZE

    def reset(self):
        self.x = self.init_x
        self.y = self.init_y
        self.angle = random.randint(60, 120)

    def cooldown(self, duration):
        self.cooldown_time = duration