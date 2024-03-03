import curses
import logger
import socket
import threading


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
        while True:
            input_string = self.get_input()
            self.output_win.refresh()
            self.input_win.refresh()
            if input_string in ["exit", "quit", "q"]:
                break
            else:
                sock.send(input_string.encode())
                self.output_win.addstr("\n" + input_string + "\n")
                self.output_win.refresh()
                self.input_win.refresh()
        sock.send("q".encode())
        self.close = True

    def create_client(self, hostname, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect((hostname, port))
                send_thread = threading.Thread(target=self.send_message, args=((sock,)), daemon=True)
                send_thread.start()
                while True:
                    data = sock.recv(1024)
                    if self.close:
                        self.logger.info("Closing client, server responded with: %s"%data.decode('utf-8'))
                        break
                    if data:
                        self.output_win.addstr("\n    %s\n"%data.decode())
                        self.output_win.refresh()
                        self.input_win.refresh()

            except KeyboardInterrupt:
                self.logger.info("Shutting down client")
                sock.send("q".encode())
                data = sock.recv(1024)
                self.logger.info('received from server: %s' %data.decode('utf-8'))
            except BrokenPipeError:
                self.logger.info("Connection to server broken, shutting down client")

            self.logger.info("Shutting down client finally")
            sock.close()


if __name__ == "__main__":
    curses.wrapper(TerminalApp)
