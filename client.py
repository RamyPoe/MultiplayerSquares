import pygame
from pygame.locals import *
import socket
from network import Network

class player:
    def __init__(self, x, y):
        self.color = (255, 0, 0)
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.velocity = 5
    
    def draw(self, color=(255, 0, 0)):
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

    def move(self, input):
        if input == 0:
            self.x -= self.velocity
        elif input == 1: 
            self.x += self.velocity
        elif input == 2:
            self.y -= self.velocity
        elif input == 3:
            self.y += self.velocity

def parseData(data):
    data = data.split(':')
    data = data[-1].split(',')
    return data[0], data[1]

def send_posData():
    data = str(network.id) + ':' + str(player0.x) + ',' + str(player0.y)
    reply = network.send(data) #network.send(data) 
    return reply

def ShowFps():
    frames = clock.get_fps() #gets fps from timer
    font = pygame.font.SysFont('arial', 24) #creates a font
    fpsSurf = font.render(str(int(frames)), False, (255, 255, 255), (100, 100, 100)) #renders the font with the fps
    screen.blit(fpsSurf, (0, 0)) #blit the surface onto the screen

pygame.init()

screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

network = Network()
player0 = player(0, 0)
player1 = player(70, 70)

def drawBackground():
    screen.fill((255, 255, 255))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            network.disconnect()

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and player0.x > 0:
        player0.move(0)
    if keys[pygame.K_RIGHT] and player0.x < 600-player0.width:
        player0.move(1)
    if keys[pygame.K_UP] and player0.y > 0:
        player0.move(2)
    if keys[pygame.K_DOWN] and player0.y < 400-player0.height:
        player0.move(3)

    #send pos to server

    x2, y2 = parseData(send_posData()) #send_posData()
    x2 = int(x2); y2 = int(y2)
    player1.x, player1.y = x2, y2

    print(player1.x, player1.y)

    drawBackground()
    player0.draw()
    player1.draw((0, 0, 255))
    clock.tick(60)
    ShowFps()
    pygame.display.update()