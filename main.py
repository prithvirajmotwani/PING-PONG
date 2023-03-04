import pygame
import random
from pygame import mixer

# initialize
pygame.init()

# screen
screen = pygame.display.set_mode((900, 600))

# title
pygame.display.set_caption("pong")

# icon
icon = pygame.image.load("ping-pong-icon.png")
pygame.display.set_icon(icon)

# background
background = pygame.image.load("background.png")

# pads

pad1Image = pygame.image.load("pad.png")
pad1X = 20
pad1Y = 268
padY_change = 4.5


def player1_pad(x, y):
    screen.blit(pad1Image, (x, y))


pad2Image = pygame.image.load("pad.png")
pad2X = 816
pad2Y = 268


def player2_pad(x, y):
    screen.blit(pad2Image, (x, y))


# ball
ballImg = pygame.image.load("beach-ball.png")
ballX = 438
ballY = 288
ballX_change = 0
ballY_change = 0


def ball_movement(x, y):
    screen.blit(ballImg, (x, y))


count = 0


def collided():
    global ballX, ballY, pad1X, pad1Y, ballX_change, pad2X, pad2Y, count
    pad1_rect = pygame.Rect(pad1X + 35, pad1Y, 1, 64)
    pad2_rect = pygame.Rect(pad2X + 27, pad2Y, 1, 64)
    ball_rect = pygame.Rect(ballX, ballY, 24, 24)
    count += 1
    if (pad1_rect.colliderect(ball_rect) or pad2_rect.colliderect(ball_rect)) and count > 100:
        ballX_change *= -1
        count = 0
        bounce_sound = mixer.Sound("pong bounce-2.wav")
        bounce_sound.play()


# display score
player1_score = 0
font = pygame.font.Font("freesansbold.ttf", 30)
score1_X = 225
score1_Y = 10

player2_score = 0
font = pygame.font.Font("freesansbold.ttf", 30)
score2_X = 675
score2_Y = 10


def score_display(x1, y1, x2, y2):
    score1 = font.render(str(player1_score), True, (0, 0, 0))
    screen.blit(score1, (x1, y1))

    score2 = font.render(str(player2_score), True, (0, 0, 0))
    screen.blit(score2, (x2, y2))


# obstacles
brickX = []
brickY = []


def gen_bricks():
    global brickX, brickY
    for i in range(1, 5):
        for j in range(5):
            brickX.append(180 + (j * 130))
            brickY.append(i * 115)


def draw_bricks():
    global brickX, brickY
    for i in range(len(brickX)):
        pygame.draw.rect(screen, (40, 80, 255), pygame.Rect(brickX[i], brickY[i], 20, 40))


def collide():
    global brickX, brickY, ballX_change, ballY_change
    for i in range(len(brickX)):
        top = pygame.Rect(brickX[i], brickY[i], 20, 1)
        bottom = pygame.Rect(brickX[i], brickY[i] + 39, 20, 1)
        left = pygame.Rect(brickX[i], brickY[i], 1, 40)
        right = pygame.Rect(brickX[i] + 19, brickY[i], 1, 40)
        ball_rect = pygame.Rect(ballX, ballY, 24, 24)
        if ball_rect.colliderect(top) or ball_rect.colliderect(bottom):
            ballY_change *= -1
            pop(i)
            bounce_sound = mixer.Sound("pong bounce-2.wav")
            bounce_sound.play()
            break
        if ball_rect.colliderect(right) or ball_rect.colliderect(left):
            ballX_change *= -1
            pop(i)
            bounce_sound = mixer.Sound("pong bounce-2.wav")
            bounce_sound.play()
            break


def pop(i):
    global brickX, brickY
    brickY.pop(i)
    brickX.pop(i)


gen_bricks()
running = True
while running:

    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and ballX == 438 and ballY == 288 and ballX_change == 0 and ballY_change == 0:
                ballX_change = (random.randint(4, 5)) * (-1) ** random.randint(1, 2)
                ballY_change = (random.randint(4, 5)) * (-1) ** random.randint(1, 2)

    userinput = pygame.key.get_pressed()

    if userinput[pygame.K_w]:
        pad1Y -= padY_change
    if userinput[pygame.K_s]:
        pad1Y += padY_change
    if userinput[pygame.K_UP]:
        pad2Y -= padY_change
    if userinput[pygame.K_DOWN]:
        pad2Y += padY_change

    # boundary
    if pad1Y >= 534:
        pad1Y = 534
    if pad2Y >= 534:
        pad2Y = 534
    if pad1Y <= 2:
        pad1Y = 2
    if pad2Y <= 2:
        pad2Y = 2

    if ballY <= 0:
        ballY_change = ballY_change * (-1)
    if ballY >= 587:
        ballY_change = ballY_change * (-1)
    if ballX <= 0 or ballX >= 882:
        ballX = 438
        ballY = 288
        ballX_change = 0
        ballY_change = 0

    ballX += ballX_change
    ballY += ballY_change

    if ballX <= 0:
        player2_score += 1
    if ballX >= 882:
        player1_score += 1

    player1_pad(pad1X, pad1Y)
    player2_pad(pad2X, pad2Y)
    ball_movement(ballX, ballY)
    collided()
    score_display(score1_X, score1_Y, score2_X, score2_Y)
    collide()
    draw_bricks()
    if len(brickX) == 0 and (ballX <= 0 or ballX >= 882):
        gen_bricks()

    pygame.display.update()
