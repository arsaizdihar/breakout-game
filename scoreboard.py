import pygame
from constant import *


class ScoreBoard:
    def __init__(self):
        self.score = 0
        self.life = LIFE_START
        self.font = pygame.font.SysFont('Agency FB', 50)
        self.left_rect = pygame.rect.Rect(0, 0, WIDTH / 2, SCOREBOARD_HEIGHT)
        self.right_rect = pygame.rect.Rect(WIDTH / 2, 0, WIDTH / 2, SCOREBOARD_HEIGHT)
        self.game_rect = pygame.rect.Rect(0, 0, WIDTH, HEIGHT)

    def draw(self, window):
        pygame.draw.rect(window, 'white', self.game_rect, LINE_HEIGHT)
        pygame.draw.rect(window, 'white', self.left_rect, LINE_HEIGHT)
        pygame.draw.rect(window, 'white', self.right_rect, LINE_HEIGHT)
        score_label = self.font.render(f'SCORE: {self.score}', True, (255, 255, 255))
        window.blit(score_label, (self.right_rect.centerx-score_label.get_width()/2,
                                  self.right_rect.centery-score_label.get_height()/2))
        life_label = self.font.render("LIFE: ", True, (255, 255, 255))
        life_rect = window.blit(life_label, (SIZE*2, 0))
        for i in range(self.life):
            pygame.draw.rect(window, 'green', (life_rect.right + SIZE + i*SIZE*1.5, SIZE, SIZE,
                                               SCOREBOARD_HEIGHT-SIZE*2))

