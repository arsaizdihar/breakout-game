import pygame
from pygame.locals import *

from ball import Ball
from paddle import Paddle
from brick import Brick
from constant import *
from scoreboard import ScoreBoard

pygame.init()
pygame.display.set_caption("Breakout Game")
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.mixer.init()
break_sound = pygame.mixer.Sound('break.mp3')
dead_sound = pygame.mixer.Sound('dead.mp3')
blip_sound = pygame.mixer.Sound('blip.wav')
shot_sound = pygame.mixer.Sound('shot.mp3')
health_sound = pygame.mixer.Sound('health.mp3')

heart_img = pygame.image.load('heart.png')
heart_img = pygame.transform.scale(heart_img, (HEART_SIZE, HEART_SIZE))


def game():
    ball_vel = 8
    player_vel = 15
    is_running = True
    player = Paddle((WIDTH//2)-(SIZE*4), HEIGHT-SIZE*3)
    ball = Ball(player.get_rect().centerx, player.get_rect().top - SIZE)
    scoreboard = ScoreBoard()
    clock = pygame.time.Clock()
    bricks = []
    hearts = []

    def make_bricks():
        for i in range(5):
            for j in range(WIDTH//(BRICK_WIDTH+SIZE//2)-2):
                brick_x = (j+1)*(BRICK_WIDTH+SIZE//2) + SIZE
                brick_y = (i+4)*BRICK_HEIGHT*3//2 + SCOREBOARD_HEIGHT
                bricks.append(Brick(brick_x, brick_y, scoreboard.level))
    make_bricks()

    def redraw_window():
        window.fill('black')
        player.draw(window)
        for brick in bricks:
            brick.draw(window)
        ball.draw(window)
        for bullet in player.bullets:
            if bullet.check_out_of_window():
                player.bullets.remove(bullet)
            elif bullet.check_brick_collision(bricks, hearts):
                if len(bricks) == 0:
                    scoreboard.level += 1
                    ball.reset()
                    player.reset()
                    ball.cooldown(1500)
                    make_bricks()
                scoreboard.score += 10
                player.bullets.remove(bullet)
                break_sound.play()
            else:
                bullet.draw(window, dt*ball_vel)
        for heart in hearts:
            heart.move(dt*ball_vel/2)
            if heart.check_collision(player):
                scoreboard.life += 1
                health_sound.play()
                hearts.remove(heart)
            elif heart.check_out_of_window():
                hearts.remove(heart)
            heart.draw(window, heart_img)
        scoreboard.draw(window)
        pygame.display.flip()

    while is_running:
        dt = clock.tick(FPS) / 16
        player.shoot_cooldown -= dt*16
        if ball.player_collision(player):
            blip_sound.play()
        if ball.brick_collision(bricks, hearts):
            break_sound.play()
            scoreboard.score += 10
            if len(bricks) == 0:
                scoreboard.level += 1
                ball.reset()
                player.reset()
                ball.cooldown(1500)
                make_bricks()
        ball.move(dt*ball_vel, dt, blip_sound)
        if ball.check_dead():
            dead_sound.play()
            ball.reset()
            player.reset()
            scoreboard.life -= 1
            if scoreboard.life == 0:
                is_running = False
            ball.cooldown(1500)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                pass
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_RIGHT]:
            player.right(dt*player_vel)
        if key_pressed[K_LEFT]:
            player.left(dt*player_vel)
        if key_pressed[K_SPACE]:
            player.shoot(shot_sound)


game()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

