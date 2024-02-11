# client.py
'''
    Client follows the following sequence.

    - socket.socket() - to create a socket.
    - connect((HOST, PORT)) - to connect to the HOST.
    - send / recv - based on what needs to be communicated.
'''


import socket
import logger


HOST = ''
PORT = 3874


class Client:
    def __init__(self):
        self.logger = logger.Logger().logger

    def start_client(self, hostname, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((hostname, port))
                input_string = input("> ")
                while input_string != "exit":
                    sock.send(input_string.encode())
                    input_string = input("> ")
                data = sock.recv(1024)
                self.logger.info('received from server %s' %repr(data.decode('utf-8')))
        except BrokenPipeError:
            self.logger.info("Connection to server broken, shutting down client")
        except KeyboardInterrupt:
            self.logger.info("Shutting down")
        self.logger.info("Connection closed")


if __name__=='__main__':
    client = Client()
    client.start_client(HOST, PORT)
