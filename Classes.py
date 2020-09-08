import pygame
import random
import math

class Bullet( object ):
    def __init__( self, x, y, radius, color ):
        self.x = x
        self.y = y
        self.speed = 20
        self.radius = radius
        self.color = color
        self.hitbox = ( self.x, self.y, self.radius )
        self.die = False
    
    def draw(self, window):
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
        self.hp = 20
        self.ammo = 20
        self.xdir = 0
        self.ydir = 0

    def draw(self, window, font):
        self.move()
        self.hitbox = ( self.x, self.y, self.width, self.height )
        pygame.draw.rect( window, ( 0,255,0 ), ( self.x, self.y, self.width, self.height ) )
        
        ammoText = font.render( str(self.ammo), True, ( 255,255,255 ) )
        window.blit( ammoText, ( 475, 10 ) )

        pygame.draw.rect( window, ( 100,100,100 ), ( 10,10,100,15 ) )
        pygame.draw.rect( window, ( 255,0,0 ), ( 10,10,5 * self.hp,15 ) )

    def move(self):
        if self.xdir > 0: # right
            self.x += self.speed
        elif self.xdir < 0: # left
            self.x -= self.speed

        if self.ydir > 0: # down
            self.y += self.speed
        elif self.ydir < 0: # up
            self.y -= self.speed
    
    def shoot(self, bullets):
        if self.ammo > 0:
            self.ammo -= 1
            bullets.append( Bullet( round(self.x + ( self.width / 2 )), self.y, 5, ( 255,255,255 ) ) )
    
    def hit(self):
        if self.hp > 0:
            self.hp -= 1

class Enemy(object):
    def __init__( self, x, y, width, height ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 7
        self.xdir = 0
        self.hitbox = ( self.x, self.y, self.width, self.height )
        self.canDamage = True
        self.die = False

    def draw(self, args):
        # args: 0 = window, 1 = screenSize
        self.move(args[1])
        self.hitbox = ( self.x, self.y, self.width, self.height )
        pygame.draw.rect( args[0], ( 255,0,0 ), ( self.x, self.y, self.width, self.height ) )

    def move(self, screenSize):
        if self.y < screenSize[1] + self.height:
            self.y += self.speed
        else:
            self.die = True
        
        if self.xdir < 0:
            self.x -= math.floor(self.speed / 3)
        elif self.xdir > 0:
            self.x += math.floor(self.speed / 3)
        
        if self.x + self.width >= screenSize[0]:
            self.xdir = -1
        elif self.x <= 0:
            self.xdir = 1