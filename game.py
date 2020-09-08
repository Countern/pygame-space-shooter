import pygame
import os
import random

pygame.init()

# Main Variables
screenSize = ( 500, 500 )
score = 0
spawnCount = 0
canShoot = True
shootCount = 0
font = pygame.font.SysFont( None, 24 )

window = pygame.display.set_mode(screenSize)
clock = pygame.time.Clock()
pygame.display.set_caption("Counter's Planet Defender")

# Image Variables
backgroundImage = pygame.image.load( os.path.join( "sprites", "canvas_background.png" ) )

# Classes
class Bullet( object ):
    def __init__( self, x, y, radius, color ):
        self.x = x
        self.y = y
        self.speed = 20
        self.radius = radius
        self.color = color
        self.hitbox = ( self.x, self.y, self.radius )
        self.die = False
    
    def draw(self):
        self.move()
        self.hitbox = ( self.x, self.y, self.radius )
        pygame.draw.circle( window, self.color, ( self.x, self.y ), self.radius )
    
    def move(self):
        if self.y >= 0 - self.radius:
            self.y -= self.speed
        else:
            self.die = True

class Player( object ):
    def __init__( self, x, y, width, height ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 12
        self.hitbox = ( self.x, self.y, self.width, self.height )
        self.hp = 100
        self.ammo = 20
        self.xdir = 0
        self.ydir = 0

    def draw(self):
        self.move()
        self.hitbox = ( self.x, self.y, self.width, self.height )
        pygame.draw.rect( window, ( 0,255,0 ), ( self.x, self.y, self.width, self.height ) )

    def move(self):
        if self.xdir > 0: # right
            self.x += self.speed
        elif self.xdir < 0: # left
            self.x -= self.speed
        if self.ydir > 0: # down
            self.y += self.speed
        elif self.ydir < 0: # up
            self.y -= self.speed
    
    def shoot(self):
        #if self.ammo > 0:
            #self.ammo -= 1
        bullets.append( Bullet( round(self.x + ( self.width / 2 )), self.y, 5, ( 255,255,255 ) ) )
    
    def hit(self):
        print("I've been hit by an enemy!")

class Enemy(object):
    def __init__( self, x, y, width, height ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 10
        self.hitbox = ( self.x, self.y, self.width, self.height )
        self.canDamage = True
        self.die = False

    def draw(self):
        self.move()
        self.hitbox = ( self.x, self.y, self.width, self.height )
        pygame.draw.rect( window, ( 255,0,0 ), ( self.x, self.y, self.width, self.height ) )

    def move(self):
        if self.y < screenSize[1] + self.height:
            self.y += self.speed
        else:
            self.die = True

# Functions
def DrawWindow():
    window.fill( (0,0,0) )
    player.draw()
    for enemy in enemies:
        enemy.draw()
    for bullet in bullets:
        bullet.draw()

    pygame.display.update()
def SpawnEnemy():
    enemy = Enemy( 0,0, 40, 60 )
    enemy.x = random.randint( 0, screenSize[1] - enemy.width )
    enemy.y = 0 - enemy.height
    enemies.append( enemy )

player = Player( round(screenSize[0] / 2), 420, 40, 60 )
enemies = []
bullets = []

running = True
while running:
    clock.tick(30)
    spawnCount += 1
    if spawnCount >= 50:
        SpawnEnemy()
        spawnCount = 0
    
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

    # Player movement handler
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
        player.shoot()

    # Drawing Handler
    DrawWindow()

pygame.quit()
