# client.py
'''
    Client follows the following sequence.

    - socket.socket() - to create a socket.
    - connect((HOST, PORT)) - to connect to the HOST.
    - send / recv - based on what needs to be communicated.
'''

import logger
import socket
import threading
import time


HOST = ''
PORT = 3874


class Client:
    def __init__(self):
        self.logger = logger.Logger().logger
        self.THREAD_CLOSE = False

    def send_message(self, hostname, port):
        # write code for sending message here.
        pass

    def receive_message(self, sock):
        """Receive messages indefinitely."""
        while True:
            data = sock.recv(1024)
            if data:
                self.logger.info(">>>>> %s\n" %data.decode())
            if self.THREAD_CLOSE:
                break

    def start_client(self, hostname, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((hostname, port))
            receive_thread = threading.Thread(target=self.receive_message, args=((sock,)), daemon=True)
            receive_thread.start()
            try:
                input_string = input("> ")
                while True:
                    if input_string not in ["exit", "quit", "q"]:
                        sock.send(input_string.encode())
                    else:
                        sock.send(input_string.encode())
                        break
                    # self.logger.info('received from server %s' %repr(data.decode('utf-8')))
                    input_string = input("> ")
            except KeyboardInterrupt:
                self.logger.info("Shutting down client")
                sock.send("q".encode())
                data = sock.recv(1024)
                self.logger.info('received from server %s' %repr(data.decode('utf-8')))
                sock.close()
            except BrokenPipeError:
                self.logger.info("Connection to server broken, shutting down client")
                sock.close()
            self.THREAD_CLOSE = True
            time.sleep(3)
            sock.close()
        self.logger.info("Connection closed")


if __name__=='__main__':
    client = Client()
    client.start_client(HOST, PORT)
