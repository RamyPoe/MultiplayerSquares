import socket
import pygame

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = '192.168.0.16' #ENTER IPV4 ADDRESS
        self.port = 5050
        self.addr = (self.host, self.port)
        self.format = 'utf-8'
        self.id = self.connect()
        print(self.id)

    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(2048).decode(self.format)

    def send(self, msg):
        try:
            self.client.send(msg.encode(self.format))
            otherPos = self.client.recv(2048).decode(self.format)
            return otherPos
        except socket.error as e:
            return str(e)

    def disconnect(self):
        self.send("bibi")