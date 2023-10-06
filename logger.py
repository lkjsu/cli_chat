# logger.py


import logging


class Logger:
    def __init__(self):
        logging.basicConfig()
        logging.root.setLevel(logging.INFO)
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('chat-app')
