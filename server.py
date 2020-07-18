import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
PORT = 5050
ADDR = (IP, PORT)

server.bind(ADDR)
print(f"[SERVER] Running on {socket.gethostname()} at {IP}:{PORT}")

curId = '0'
pos = ['0:0,0', '1:70,70']

def handle_client(conn, addr):
    global pos, curId
    print(f"[NEW CONNECTION] {addr} connected")

    conn.send(curId.encode(FORMAT))
    curId = '1'
    while True:
        
        try:
            data = conn.recv(2048).decode(FORMAT)
            # print(data)
            if not data:
                print(f"[DISCONNECT] {addr} has disconnected")
                break
            else:
                if data == "bibi":
                    print(f"[DISCONNECT] {addr} has disconnected")
                    conn.close()
                    break
                else:
                    i = data.split(':')
                    if i[0] == '0':
                        pos[0] = data
                        conn.send(pos[1].encode(FORMAT))
                    elif i[0] == '1':
                        pos[1] = data
                        conn.send(pos[0].encode(FORMAT))
                    print(pos)

        except:
            conn.close()
            print(f"[DISCONNECT] {addr} has disconnected")
            break


def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()

start()