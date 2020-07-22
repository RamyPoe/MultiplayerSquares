import pygame
from pygame.locals import *
import socket
import time
from tkinter import *
import tkinter.messagebox as tm
import os
import sys

class Network:
    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = ip #ENTER IPV4 ADDRESS
        self.port = port
        self.addr = (self.host, int(self.port))
        self.format = 'utf-8'
        self.id = self.connect()
        print(self.id)

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode(self.format)
        except:
            quit()
    
    def wait(self):
        msg = self.client.recv(2048).decode(self.format)
        if msg != 'start':
            self.wait()

    def send(self, msg):
        try:
            self.client.send(msg.encode(self.format))
            otherPos = self.client.recv(2048).decode(self.format)
            # print(otherPos)
            return otherPos
        except socket.error as e:
            return str(e)

    def disconnect(self):
        self.send("bibi")

class player:
    def __init__(self, x, y):
        self.color = (255, 0, 0)
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.velocity = 5
        self.it = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if self.it == True:
            pygame.draw.rect(screen, (255, 0, 0), self.rect)
        else:
            pygame.draw.rect(screen, (0, 0, 255), self.rect)
        

    def move(self, input):
        if input == 0:
            self.x -= self.velocity
        elif input == 1: 
            self.x += self.velocity
        elif input == 2:
            self.y -= self.velocity
        elif input == 3:
            self.y += self.velocity

def goInfo():
    try:
        os.remove('dependencies/info.txt')
    except:
        pass

    f = open('dependencies/info.txt', 'w+')

    class LoginFrame(Frame):
        def __init__(self, master):
            super().__init__(master)

            self.label_username = Label(self, text="IPV4")
            self.label_password = Label(self, text="PORT")

            self.entry_username = Entry(self)
            self.entry_password = Entry(self)

            self.label_username.grid(row=0, sticky=E)
            self.label_password.grid(row=1, sticky=E)
            self.entry_username.grid(row=0, column=1)
            self.entry_password.grid(row=1, column=1)

            self.logbtn = Button(self, text="OK", command=self._login_btn_clicked)
            self.logbtn.grid(columnspan=2)

            root.minsize(250, 75)
            root.wm_title('Enter Your Info')

            self.pack()

        def _login_btn_clicked(self):
            # print("Clicked")

            ipv4 = self.entry_username.get()
            port = self.entry_password.get()

            f.write(f"{ipv4}\n{port}")
            f.close()
            root.destroy()

    root = Tk()
    lf = LoginFrame(root)
    root.mainloop()

def retrieveInfo():
    f = open('dependencies/info.txt', 'r')
    info = f.read()
    info = info.splitlines()
    f.close()
    return info[0], info[1]

def parseData(data):
    print(data)
    if data:
        touching = data.split(':')[1].split('.')[-1]
        data = data.split(':')[1].split('.')[0].split(',')
        return data[0], data[1], touching
    else:
        return player1.x, player1.y, '0'

def send_posData():
    data = str(network.id) + ':' + str(player0.x) + ',' + str(player0.y)
    reply = network.send(data) #network.send(data) 
    return reply

def ShowFps():
    frames = clock.get_fps() #gets fps from timer
    font = pygame.font.SysFont('arial', 24) #creates a font
    fpsSurf = font.render(str(int(frames)), False, (255, 255, 255), (100, 100, 100)) #renders the font with the fps
    screen.blit(fpsSurf, (0, 0)) #blit the surface onto the screen

def itTime(msg):
    font = pygame.font.SysFont('arial', 30) #creates a font
    timeSurf = font.render(msg, False, (0, 0, 0)) #renders the font with the fps
    screen.blit(timeSurf, (285, 0)) #blit the surface onto the screen

loaded = True

def drawBackground():
    screen.fill((255, 255, 255))

#Start Pygame-----------------------------------------------------------------------------
pygame.init()

monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]

finalScreen = pygame.display.set_mode((640, 360))
screen = pygame.Surface((640, 360))
icon = pygame.image.load('dependencies/icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('MultiPlayer Tag!')
clock = pygame.time.Clock()

#Creating things-----------------------------------------------------------------------------
goInfo()
ip, port = retrieveInfo()
network = Network(ip, port)

try:
    taggedSfx = pygame.mixer.music.load("dependencies/song.wav")
except:
    loaded = False

if network.id == '0':
    player0 = player(0, 0)
    player1 = player(pygame.display.Info().current_w-50, pygame.display.Info().current_h-50)
    player0.it = False
    player1.it = True
elif network.id == '1':
    player0 = player(pygame.display.Info().current_w-50, pygame.display.Info().current_h-50)
    player1 = player(0, 0)
    player0.it = True
    player1.it = False

startTimer = False

start_time = time.time()
start_time = int(start_time)

progress = 10
#In queue--------------------------------------------------------------------
def queue():
    font = pygame.font.SysFont('arial', 50) #creates a font
    waiting = font.render("Waiting for another player...", False, (255, 255, 255)) #renders the font with the fps
    screen.fill((100, 100, 100))
    screen.blit(waiting, (320-int(waiting.get_width()/2), 180-int(waiting.get_height()/2))) #blit the surface onto the screen
    finalScreen.blit(screen, (0, 0))
    pygame.display.update()

    network.wait()
queue()

if loaded:
    pygame.mixer.music.play(-1)
#Main Loop--------------------------------------------------------------------
fullscreen = False
goMain = True
while goMain:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            goMain = False

    #Local Movement------------------------------------------------------
    keys = pygame.key.get_pressed()

    if keys[pygame.K_F11]:
        fullscreen = not fullscreen
        if fullscreen:
            finalScreen = pygame.display.set_mode((monitor_size), pygame.FULLSCREEN)
        else:
            finalScreen = pygame.display.set_mode((640, 360))
    if keys[pygame.K_LEFT] and player0.x > 0:
        player0.move(0)
    if keys[pygame.K_RIGHT] and player0.x < pygame.display.Info().current_w-player0.width:
        player0.move(1)
    if keys[pygame.K_UP] and player0.y > 0:
        player0.move(2)
    if keys[pygame.K_DOWN] and player0.y < pygame.display.Info().current_h-player0.height:
        player0.move(3)

    #send pos to server and update other player's pos-----------
    x2, y2, colliding = parseData(send_posData())
    x2 = int(x2); y2 = int(y2)
    player1.x, player1.y = x2, y2

    #Check for collisions--------------------------------------------------
    if colliding == '0':
        touching = False
        if startTimer:
            progress = 10-(int(time.time())-start_time)

    elif colliding == '1' and touching == False:
        touching = True
        startTimer = True
        start_time = time.time()
        start_time = int(start_time)

        if player0.it == True:
            player0.it = False
            player1.it = True
        else:
            player0.it = True
            player1.it = False

    if startTimer:
        progress = 10-(int(time.time())-start_time)

    drawBackground()
    player0.draw()
    player1.draw()
    itTime(str(progress))
    # ShowFps()
    
    #Check For Winner----------------------------------------------------------
    if progress == 0:
        font = pygame.font.SysFont('arial', 40, 1) #creates a font
        if player0.it == False:
            Surf = font.render("YOU WIN!!!", False, (255, 255, 255), (100, 100, 100)) #renders the font with the fps

        elif player0.it == True:
            Surf = font.render("YOU LOSE!!!", False, (255, 255, 255), (100, 100, 100)) #renders the font with the fps

        screen.fill((100, 100, 100))
        screen.blit(Surf, (640/2-Surf.get_width()/2, 360/2-Surf.get_height()/2)) #blit the surface onto the screen

        startTimer = False
        progress = 10
            
        if fullscreen:
            pygame.transform.scale(screen, (monitor_size), finalScreen)
        else:
            finalScreen.blit(screen, (0, 0))
        pygame.display.update()

        if network.id == '0':
            player0 = player(0, 0)
            player1 = player(640-50, 360-50)
            player0.it = False
            player1.it = True
        elif network.id == '1':
            player0 = player(640-50, 360-50)
            player1 = player(0, 0)
            player0.it = True
            player1.it = False
        time.sleep(4)

    clock.tick(60)
    pygame.display.update()
    if fullscreen:
        pygame.transform.scale(screen, (monitor_size), finalScreen)
    else:
        finalScreen.blit(screen, (0, 0))

pygame.quit()
network.disconnect()