import socket
import time

'''
    Server follows the following sequence while opening up connections.

    - socket.socket(arg1, arg2) - arg1 is usually AF_INET which is IPv4, arg2 is usually SOCK_STREAM ( tcp ) or DGRAM ( udp ).
    - bind((HOST, PORT)) - HOST stands for hostname and the PORT for port on which server listens.
    - listen(backlog) - backlog is how many connections it can allow before it refuses.
    - accept() - accepts a connection and then sends communication over network.
'''

HOST = ''
PORT = 3874

class Server:
    connections = []

    def run_server_forever(self, hostname, port, backlog_connections_allowed):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((hostname, port))
            sock.listen(backlog_connections_allowed)
            try:
                while True:
                    conn, addr = sock.accept()
                    with conn:
                        print("Connection made", addr)
                        while True:
                            data = conn.recv(1024)
                            if not data: break
                            print("Value received", data)
                            conn.send(b'OK')
            except KeyboardInterrupt:
                print('Shutting down server...')
                time.sleep(3)
        print('Connection closed.')

if __name__=='__main__':
    server = Server()
    server.run_server_forever(HOST, PORT, 5)
