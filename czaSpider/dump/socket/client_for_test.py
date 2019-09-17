import socket, json, time

HOST = '127.0.0.1'  ##
PORT = 8022

tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpCliSock.connect((HOST, PORT))
tcpCliSock.send(json.dumps({'cookie': 'test', 'user':'test'}).encode())

while True:
    print(json.loads(tcpCliSock.recv(1024).decode()))
    message = input('输入聊天内容')
    tcpCliSock.send(json.dumps({'state': 11, 'message': message, 'to': 'cza'}).encode())

