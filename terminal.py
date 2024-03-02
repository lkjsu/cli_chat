import curses
import logger
import socket
import threading
import sys

HOST = '0.0.0.0'
PORT = 3874

class TerminalApp:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.logger = logger.Logger().logger
        self.close = False
        curses.curs_set(1)  # Hide the cursor

        curses.use_default_colors()
        # Get the background color of the terminal
        self.bg_color = curses.color_pair(0)

        # Create a window for user input
        self.input_win = curses.newwin(1, curses.COLS, curses.LINES-1, 0)
        self.input_win.addstr(0, 0, ">>> ", self.bg_color)
        self.input_win.refresh()

        # Create a window for displaying output
        self.output_win = curses.newwin(curses.LINES-1, curses.COLS, 0, 0)

        self.create_client(HOST, PORT)

    def run(self):
        try:
            while True:
                # Get user input
                user_input = self.get_input()
                if user_input in ["q", "quit", "exit"]:
                    break

                # Display the entered command in the output area
                self.output_win.addstr(f">>> {user_input}\n", self.bg_color)
                self.output_win.refresh()

                # Execute the command
                result = self.run_command(user_input)

                # Display the result in the output area
                self.output_win.addstr(f"{result}\n", self.bg_color)
                self.output_win.refresh()

        except KeyboardInterrupt:
            self.logger.info("Shutting down client.")
            

    def get_input(self):
        # Allow the user to enter input
        curses.echo()
        user_input = self.input_win.getstr(0, 4).decode('utf-8')
        curses.noecho()

        # Clear the input box
        self.input_win.clear()
        self.input_win.addstr(0, 0, ">>> ", self.bg_color)
        self.input_win.refresh()

        return user_input.strip()

    def run_command(self, command):
        # Implement your logic for command execution here
        # This is a placeholder; replace it with your own code
        return f"Command executed: {command}"

    def send_message(self, sock):
        # write code for sending message here.
        try:
            while True:
                input_string = self.get_input()
                self.input_win.refresh()
                if input_string not in ["exit", "quit", "q"]:
                    sock.send(input_string.encode())
                    self.output_win.addstr(str(sock.getpeername()[1]) + "\n" + input_string + "\n")
                    self.output_win.refresh()
                    self.input_win.refresh()
                else:
                    sock.send(input_string.encode())
                    break
                self.output_win.refresh()
                self.input_win.refresh()

        except KeyboardInterrupt:
            self.logger.info("Shutting down client")
            sock.send("q".encode())
            data = sock.recv(1024)
            self.logger.info('received from server %s' %repr(data.decode('utf-8')))
        except BrokenPipeError:
            self.logger.info("Connection to server broken, shutting down client")
        self.close = True

    def create_client(self, hostname, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((hostname, port))
            send_thread = threading.Thread(target=self.send_message, args=((sock,)), daemon=True)
            send_thread.start()
            while True:
                data = sock.recv(1024)
                if data:
                    self.output_win.addstr("\n    %s\n"%data.decode())
                    self.output_win.refresh()
                    self.input_win.refresh()
                if self.close:
                    break
            sock.close()

if __name__ == "__main__":
    curses.wrapper(TerminalApp)
