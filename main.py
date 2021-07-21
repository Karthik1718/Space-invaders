import pygame
import random
import math
from pygame import mixer

#Initialize the pygame
pygame.init()

#music
background = mixer.music.load("background.wav")
mixer.music.play(-1)

#create the screen
screen = pygame.display.set_mode((432, 500))
bgImg = pygame.image.load("spaceship_bg.jpg")

#title and icon
pygame.display.set_caption("Space Invadors")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load("player.png")
playerX = 190
playerY = 440
playerX_change = 0

#enemy
enemyImg =[]
enemyX = []
enemyY =[]
enemyX_change =[]
enemyY_change =[]
no_of_enemy =6

for i in range(no_of_enemy):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 468))
    enemyY.append(random.randint(0, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(45)



#bullet1
bulletImg1 = pygame.image.load("bullet1.png")
bulletX1 = 0
bulletY1 = playerY
bullet_state1 = "ready"
bulletY_change = 0.4

#bullet2
bulletImg2 = pygame.image.load("bullet2.png")
bulletX2 = 0
bulletY2 = playerY
bullet_state2 = "ready"

#text
score =0
font = pygame.font.Font('freesansbold.ttf' ,25)
font1 = pygame.font.Font('freesansbold.ttf' ,50)


#explosion
explosionImg = pygame.image.load("explosion.png")


def show_score():
    score_value = font.render("SCORE :"+ str(score), True, (255, 255 , 255))
    screen.blit(score_value, (10, 10))


def game_over_text():
    game_over = font1.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over, (70, 190))


def player(X,Y):
    screen.blit(playerImg, (X, Y))


def enemy(X,Y, i):
    screen.blit(enemyImg[i], (X, Y))

def explosion(x, y):
    screen.blit(explosionImg, (x, y))


def fire_bullet1(X,Y):
    global bullet_state1
    bullet_state1 = 'fire'
    screen.blit(bulletImg1, (X+16, Y-20))

def fire_bullet2(X,Y):
    global bullet_state2
    bullet_state2 = 'fire'
    screen.blit(bulletImg2, (X+16, Y-20))


def iscollision(bulletX, bulletY, enemyX, enemyY):
    distance = math.sqrt(math.pow(enemyX-bulletX, 2) + math.pow(enemyY-bulletY, 2))
    if distance < 25:
        return True


#Game loop
running = True
while running:
    # bg color
    screen.fill((0, 0, 0))
    screen.blit(bgImg, (-60,-300))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # left right movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.4
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.4
            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound("bullet.wav")
                bullet_sound.play()
                if bullet_state1 is "ready":
                    bulletX1 = playerX + playerX_change
                    fire_bullet1(bulletX1, bulletY1)
                elif bullet_state2 is "ready":
                    bulletX2 = playerX + playerX_change
                    fire_bullet2(bulletX2, bulletY2)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0



    playerX += playerX_change
    if playerX <=0:
        playerX = 0
    if playerX >=368:
        playerX = 368
    player(playerX, playerY)

    #enemy movement
    for i in range(no_of_enemy):

        # collision of player and enemy
        distance = math.sqrt(math.pow(enemyX[i] - playerX, 2) + math.pow(enemyY[i] - playerY, 2))
        if distance <= 60:
            for j in range(no_of_enemy):
                enemyY[j] = 600
            break



        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= -68:
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]
        if enemyX[i] >=468:
            enemyX_change[i] = -0.2
            enemyY[i] += enemyY_change[i]
        enemy(enemyX[i], enemyY[i], i)


        # collision of enemy and bullet
        collision1 = iscollision(enemyX[i], enemyY[i], bulletX1, bulletY1)
        collision2 = iscollision(enemyX[i], enemyY[i], bulletX2, bulletY2)
        if bullet_state1 == "fire" and collision1 == True:
            x , y = enemyX[i], enemyY[i];
            explosion(x, y)
            collision_sound = mixer.Sound("collision.wav")
            collision_sound.play()
            bulletY1 = playerY
            bullet_state1 = "ready"
            score += 1
            enemyX[i] = random.randint(0, 468)
            enemyY[i] = random.randint(0, 300)
        elif bullet_state2 == "fire" and collision2 == True:
            x , y = enemyX[i], enemyY[i];
            explosion(x, y)
            collision_sound = mixer.Sound("collision.wav")
            collision_sound.play()
            bulletY2 = playerY
            bullet_state2 = "ready"
            score += 1
            enemyX[i] = random.randint(0, 468)
            enemyY[i] = random.randint(0, 300)

    #game over
    for i in range(no_of_enemy):
        if enemyY[i] >= 600:
            game_over_text()

    #bullet  loading
    if bulletY1 <100:
        bulletY1 = playerY
        bullet_state1 = "ready"
    if bullet_state1 == "fire":
        bulletY1 -= bulletY_change
        fire_bullet1(bulletX1, bulletY1)

    if bulletY2 <100:
        bulletY2 = playerY
        bullet_state2 = "ready"
    if bullet_state2 == "fire":
        bulletY2 -= bulletY_change
        fire_bullet2(bulletX2, bulletY2)


    show_score()

    pygame.display.update()

