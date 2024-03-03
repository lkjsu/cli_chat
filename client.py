# client.py
'''
    Client follows the following sequence.

    - socket.socket() - to create a socket.
    - connect((HOST, PORT)) - to connect to the HOST.
    - send / recv - based on what needs to be communicated.
'''

import logger
import socket
import sys
import threading


HOST = ''
PORT = 3874


class Client:
    def __init__(self):
        self.logger = logger.Logger().logger
        self.close = False

    def send_message(self, sock):
        # write code for sending message here.
        try:
            input_string = input("> ")
            while True:
                if input_string not in ["exit", "quit", "q"]:
                    sock.send(input_string.encode())
                else:
                    sock.send(input_string.encode())
                    break
                input_string = input("> ")

        except KeyboardInterrupt:
            self.logger.info("Shutting down client")
            sock.send("q".encode())
            data = sock.recv(1024)
            self.logger.info('received from server %s' %repr(data.decode('utf-8')))
        except BrokenPipeError:
            self.logger.info("Connection to server broken, shutting down client")
        self.close = True

    def receive_message(self, sock):
        """Receive messages indefinitely."""
        pass

    def start_client(self, hostname, port):
        """Creates a socket to communicate with the server."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((hostname, port))
            send_thread = threading.Thread(target=self.send_message, args=((sock,)), daemon=True)
            send_thread.start()
            while True:
                data = sock.recv(1024)
                if data:
                    sys.stdout.write("\n    %s\n"%data.decode())

                if self.close:
                    break
            sock.close()
        self.logger.info("Connection closed")


if __name__=='__main__':
    client = Client()
    client.start_client(HOST, PORT)
