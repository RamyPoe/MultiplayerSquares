import pygame
from pygame.locals import *

pygame.init()

class gameRect():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect((self.x, self.y), (50, 50))

    def update(self):
        self.rect = pygame.Rect((self.x, self.y), (50, 50))

player0 = gameRect(0, 0)
player1 = gameRect(25, 25)

def colliding():
    if player0.rect.colliderect(player1):
        return '.1'
    else:
        return '.0'

print(colliding())

player1.x = 300
player1.update()

print(colliding())