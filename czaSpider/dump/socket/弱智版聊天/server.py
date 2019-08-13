import socket
host = socket.gethostname()
port = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
sock, addr = s.accept()
print('Connection built')
info = sock.recv(1024).decode()
while info != 'exit':
    print('client say: '+ info)
    send_msg = input('server now you say: ')
    sock.send(send_msg.encode())
    if send_msg == 'exit':
        break
    info = sock.recv(1024).decode()
sock.close()
s.close()