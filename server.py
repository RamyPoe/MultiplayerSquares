import socket
import threading
import datetime
import pygame

pygame.init()

class gameRect():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect((self.x, self.y), (50, 50))

    def update(self):
        self.rect = pygame.Rect((self.x, self.y), (50, 50))

player0 = gameRect(0, 0)
player1 = gameRect(550, 350)

def colliding():
    if player0.rect.colliderect(player1):
        return '.1'
    else:
        return '.0'


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
PORT = 5050
ADDR = (IP, PORT)

server.bind(ADDR)
print(f"[SERVER] Running on {socket.gethostname()} at {IP}:{PORT}")

curId = '0'
pos = ['0:0,0', '1:550,350']
bothIn = 0

def handle_client(conn, addr):
    global pos, curId, bothIn
    print(f"[NEW CONNECTION] {addr} connected")

    f = open('clients.txt', 'a+')
    f.write(f"[{datetime.datetime.now()}] {addr} CONNECTED\n")

    conn.send(curId.encode(FORMAT))
    curId = '1'
    bothIn += 1
    while bothIn != 2:
        continue

    conn.send('start'.encode(FORMAT))
    print("[GAME START] sent 'start' to both players")
    while True:
        try:
            data = conn.recv(2048).decode(FORMAT)
            # print(data)
            if not data:
                print(f"[DISCONNECT] {addr} has disconnected")
                f.write(f"[{datetime.datetime.now()}] {addr} DISCONNECTED\n")
                f.close()
                break
            else:
                if data == "bibi":
                    print(f"[DISCONNECT] {addr} has disconnected")
                    conn.close()
                    f.write(f"[{datetime.datetime.now()}] {addr} DISCONNECTED\n")
                    f.close()
                    break
                else:
                    i = data.split(':')
                    if i[0] == '0':
                        pos[0] = data
                        data = data.split(':')[1].split(',')
                        player0.x, player0.y = int(data[0]), int(data[1])
                        player0.update(); player1.update()
                        sendData = pos[1] + colliding()
                        conn.send(sendData.encode(FORMAT))
                    elif i[0] == '1':
                        pos[1] = data
                        data = data.split(':')[1].split(',')
                        player1.x, player1.y = int(data[0]), int(data[1])
                        player0.update(); player1.update()
                        sendData = pos[0] + colliding()
                        conn.send(sendData.encode(FORMAT))
                    print(pos, colliding().split('.')[-1])

        except:
            conn.close()
            print(f"[DISCONNECT] {addr} has disconnected")
            f.write(f"[{datetime.datetime.now()}] {addr} DISCONNECTED\n")
            f.close()
            break


def start():
    server.listen(2)
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()

start()