# user.py

class User:
    def __init__(self, name, friends=[]) -> None:
        self.chats = []
        self.friends = friends
        self.name = name