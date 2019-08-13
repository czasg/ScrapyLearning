import socket

s = socket.socket()
host = socket.gethostname()
port = 12345
s.connect((host, port))
print('connected')
info = ''
while info != 'exit':
    print('server say: '+ info)
    send_msg = input('client now you say: ')
    s.send(send_msg.encode())
    if send_msg == 'exit':
        break
    info = s.recv(1024).decode()
s.close()