import pygame
import os
import random
import Classes

pygame.init()

# Main Variables
screenSize = ( 500, 500 )
score = 0
spawnCount = 0
canShoot = True
shootCount = 0
font = pygame.font.SysFont( None, 24 )
random.seed(100)

window = pygame.display.set_mode(screenSize)
clock = pygame.time.Clock()
pygame.display.set_caption("Counter's Planet Defender")

# Functions
def DrawWindow():
    window.fill( (0,0,0) )
    player.draw(window, font)
    for enemy in enemies:
        enemy.draw((window, screenSize))
    for bullet in bullets:
        bullet.draw(window)

    pygame.display.update()
def SpawnEnemy():
    for x in range(4):
        positionX = random.randint(0, screenSize[1] - 40)
        enemy = Classes.Enemy(positionX,-60, 40, 60)
        if random.random() >= 0.5:
            enemy.xdir = -1
        else:
            enemy.xdir = 1
        enemies.append(enemy)

player = Classes.Player( round(screenSize[0] / 2), 420, 40, 60 )
enemies = []
bullets = []

running = True
while running:
    clock.tick(30)
    spawnCount += 1
    if spawnCount >= 50:
        SpawnEnemy()
        spawnCount = 0
    
    # Player shooting cooldown
    if canShoot == False:
        shootCount += 1
        if shootCount >= 10:
            shootCount = 0
            canShoot = True

    # Exiting Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Entity Handler
    for bullet in bullets:
        if bullet.die == True:
            bullets.pop( bullets.index( bullet ) )

    for enemy in enemies:
        for bullet in bullets:
            if enemy.hitbox[0] <= bullet.hitbox[0] + bullet.hitbox[2] and enemy.hitbox[0] + enemy.hitbox[2] >= bullet.hitbox[0] - bullet.hitbox[2]:
                if enemy.hitbox[1] <= bullet.hitbox[1] + bullet.hitbox[2] and enemy.hitbox[1] + enemy.hitbox[3] >= bullet.hitbox[1] - bullet.hitbox[2]:
                    enemy.die = True
                    bullets.pop( bullets.index( bullet ) )
        
        if player.hitbox[0] <= enemy.hitbox[0] + enemy.hitbox[2] and player.hitbox[0] + player.hitbox[2] >= enemy.hitbox[0]:
            if player.hitbox[1] <= enemy.hitbox[1] + enemy.hitbox[3] and player.hitbox[1] + player.hitbox[3] >= enemy.hitbox[1]:
                player.hit()
                enemy.die = True

        if enemy.die == True:
            enemies.pop( enemies.index(enemy) )
            break

    # Player keyse handler
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a] and player.hitbox[0] > 0:
        player.xdir = -1
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d] and player.hitbox[0] + player.hitbox[2] < screenSize[0]:
        player.xdir = 1
    else:
        player.xdir = 0

    if keys[pygame.K_UP] or keys[pygame.K_w] and player.hitbox[1] > 0:
        player.ydir = -1
    elif keys[pygame.K_DOWN] or keys[pygame.K_s] and player.hitbox[1] + player.hitbox[3] < screenSize[1]:
        player.ydir = 1
    else:
        player.ydir = 0
    
    if keys[pygame.K_SPACE] and canShoot == True:
        canShoot = False
        player.shoot(bullets)

    # Drawing Handler
    DrawWindow()

pygame.quit()