import logging

class Logger:
    def __init__(self):
        logging.basicConfig()
        logging.root.setLevel(logging.NOTSET)
        logging.basicConfig(level=logging.NOTSET)
        self.logger = logging.getLogger('chat-app')
        self.logger.setLevel(logging.INFO)