# server.py
'''
    Server follows the following sequence while opening up connections.

    - socket.socket(arg1, arg2) - arg1 is usually AF_INET which is IPv4, arg2 is usually SOCK_STREAM ( tcp ) or DGRAM ( udp ).
    - bind((HOST, PORT)) - HOST stands for hostname and the PORT for port on which server listens.
    - listen(backlog) - backlog is how many connections it can allow before it refuses.
    - accept() - accepts a connection and then sends communication over network.
'''


import socket
import logger
import threading


HOST = '0.0.0.0'
PORT = 3874


class Server:
    def __init__(self):
        self.connections = []
        self.logger = logger.Logger().logger
        self.connections = {}

    def generate_string_address(self, addr):
        """returns a string identifier for the address passed."""
        return addr[0]+':'+str(addr[1])
    
    def process_client_connection(self, connection, address):
        """
            process connection to the user.
        """
        try:
            string_address = self.generate_string_address(address)
            self.logger.info("Connection starting thread number: %s" %threading.current_thread().ident)
            while True:
                data = connection.recv(1024)
                if data.decode('utf-8') in ["exit", "quit", "q"]:
                    connection.send("OK".encode())
                    break
                self.logger.info("Connections: %s"%self.connections)
                for conn in self.connections:
                    if conn != string_address:
                        self.connections[conn].send(data)
        except KeyboardInterrupt:
            self.logger.info("Connection closing %s" %threading.current_thread().ident)
            self.connections.pop(string_address, None)
            connection.close()
        finally:
            self.logger.info("Connection closing finally %s" %threading.current_thread().ident)
            self.connections.pop(string_address, None)
            connection.close()

    def run_server_forever(self, hostname, port, backlog_connections_allowed):
        """
           runs forever to accept multiple connections.
           spawns new thread on successful connection.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((hostname, port))
            sock.listen(backlog_connections_allowed)
            try:
                while True:
                    conn, addr = sock.accept()
                    self.logger.info("Connection made -> %s",addr)
                    thread_executor = threading.Thread(target=self.process_client_connection, args=(conn, addr), daemon=True)
                    self.connections[self.generate_string_address(addr)] = conn
                    self.logger.info(self.connections)
                    thread_executor.start()
                    
            except KeyboardInterrupt:
                self.logger.info('Shutting down server...')
                sock.close()
        self.logger.info('Connection closed.')


if __name__ == '__main__':
    server = Server()
    server.run_server_forever(HOST, PORT, 1)