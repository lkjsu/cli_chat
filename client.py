import socket

'''
    Client follows the following sequence.

    - socket.socket() - to create a socket.
    - connect((HOST, PORT)) - to connect to the HOST.
    - send / recv - based on what needs to be communicated.
'''

HOST = ''
PORT = 3874

class Client:
    server_address = None

    def start_client(self, hostname, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((hostname, port))
            sock.send(b'jeriko')
            data = sock.recv(1024)
            print('received from server', repr(data))

if __name__=='__main__':
    client = Client()
    client.start_client(HOST, PORT)
