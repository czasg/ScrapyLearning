import socketserver


class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        pass


if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 8102), MyServer)
