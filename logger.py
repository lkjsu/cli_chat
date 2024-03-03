# logger.py


import logging
import os


class Logger:
    def __init__(self):
        # Create a logger
        self.logger = logging.getLogger('my_logger')
        self.logger.setLevel(logging.DEBUG)

        # Create a formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        # Create a handler for writing log messages to the console (stdout)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)  # Set the desired log level for the console output
        console_handler.setFormatter(formatter)

        # Create a handler for writing log messages to a file
        current_pid_file = "logs/" + str(os.getpid()) + ".log"
        file_handler = logging.FileHandler(current_pid_file)
        file_handler.setLevel(logging.DEBUG)  # Set the desired log level for the file output
        file_handler.setFormatter(formatter)

        # Add both handlers to the logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
