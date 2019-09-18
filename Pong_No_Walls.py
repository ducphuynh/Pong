import pygame
from pygame.locals import *
from sys import exit
import random

pygame.init()

# Screen and background
screen = pygame.display.set_mode((1280, 720), 0, 0)
back = pygame.Surface((1280, 720))
background = back.convert()
background = pygame.image.load("blue_streaks.jpg")

# Paddles
paddle = pygame.Surface((10, 50))
player = paddle.convert()
player.fill((255, 255, 255))
computer = paddle.convert()
computer.fill((255, 0, 0))

# Ball
circle_surface = pygame.Surface((30, 30))
circle = pygame.draw.circle(circle_surface, (100, 200, 0), (15, 15), 15)
circle = circle_surface.convert()
circle.set_colorkey((0, 0, 0))

# Predefined values
player_x, computer_x = 0, 1270
player_y, computer_y = 360, 360
circle_x, circle_y = 640, 360
player_move, computer_move = 0, 0
speed_x, speed_y, circle_speed = 350, 350, 350
player_score, computer_score = 0, 0
player_games_won, computer_games_won = 0, 0
paddle_hits = pygame.mixer.Sound("Nice.wav")
victory = pygame.mixer.Sound("Fanfare.wav")
defeat = pygame.mixer.Sound("defeat.wav")
keep_playing = True

# Print paddles, dashed line and score onto screen
mainClock = pygame.time.Clock()
font = pygame.font.SysFont("calibri", 80)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_UP:
                player_move = -ai_speed
            elif event.key == K_DOWN:
                player_move = ai_speed
        elif event.type == KEYUP:
            if event.key == K_UP:
                player_move = 0
            elif event.key == K_DOWN:
                player_move = 0

    score_p = font.render(str(player_score), True, (255, 255, 255))
    score_c = font.render(str(computer_score), True, (255, 255, 255))

    screen.blit(background, (0, 0))
    for x in range(5, 720, 5):
        middle_line = pygame.draw.line(screen, (255, 255, 255), (640,(x-5)*3+5), (640, x*3))
    screen.blit(player, (player_x, player_y))
    screen.blit(computer, (computer_x, computer_y))
    screen.blit(circle, (circle_x, circle_y))
    screen.blit(score_p, (580, 50))
    screen.blit(score_c, (660, 50))

    player_y += player_move

    # movement of circle
    time_passed = mainClock.tick(30)
    time_sec = time_passed / 1000

    circle_x += speed_x * time_sec
    circle_y += speed_y * time_sec
    ai_speed = circle_speed * time_sec

    # AI of the computer.
    if circle_x >= 305:
        if not computer_y == circle_y + 7.5:
            if computer_y < circle_y + 7.5:
                computer_y += ai_speed
            if computer_y > circle_y - 42.5:
                computer_y -= ai_speed
        else:
            computer_y == circle_y + 7.5

# Paddle boundaries
    if player_y >= 670:
        player_y = 670

    elif player_y <= 0:
        player_y = 0

    if computer_y >= 670:
        computer_y = 670

    elif computer_y <= 0:
        computer_y = 0

    # Point system and collision checking
    if circle_x <= player_x + 5:
        if circle_y >= player_y - 5 and circle_y <= player_y + 70:
            circle_x = 20
            speed_x = -speed_x
            pygame.mixer.Sound.play(paddle_hits)

    if circle_x >= computer_x - 5:
        if circle_y >= computer_y - 5 and circle_y <= computer_y + 70:
            circle_x = 1200
            speed_x = -speed_x
            pygame.mixer.Sound.play(paddle_hits)


    if circle_x < 5:
        computer_score += 1
        circle_x, circle_y = 660, 360
        player_y, computer_y = 360, 360

    elif circle_x > 1270:
        player_score += 1
        circle_x, circle_y = 620, 360
        player_y, computer_y = 360, 360

    if circle_y <= 0:
        speed_y = -speed_y
        circle_y = 0

    elif circle_y >= 690:
        speed_y = -speed_y
        circle_y = 690

    # Update scores, check for winners, and ask to play again

    def play_again():
        while True:
            reply = input("Do you want to play again? 'y' or 'n' ")
            if reply == "n":
                exit(0)
            if reply == "y":
                pygame.mixer.Sound.stop(victory)
                pygame.mixer.Sound.stop(defeat)
                break

    if player_score >= 11 and player_score > computer_score + 1:
        player_games_won += 1
        player_score, computer_score = 0, 0

    if computer_score >= 11 and computer_score > player_score + 1:
        computer_games_won += 1
        player_score, computer_score = 0, 0

    if player_games_won == 3:
        player_wins = font.render("Player has won!", True, (255, 255, 255))
        screen.blit(player_wins, (320, 360))
        player_games_won, computer_games_won = 0, 0
        pygame.mixer.Sound.play(victory)
        play_again()

    if computer_games_won == 3:
        computer_wins = font.render("Computer has won!", True, (255, 255, 255))
        screen.blit(computer_wins, (940, 360))
        player_games_won, computer_games_won = 0, 0
        pygame.mixer.Sound.play(defeat)
        play_again()


    pygame.display.update()