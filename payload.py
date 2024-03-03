# payload.py


class Payload:
    def __init__(self, sender_address, receiver_address, payload):
        self.sender_address = sender_address
        self.receiver_address = receiver_address
        self.payload = payload
    
    def encode_payload(self):
        self.sender_address.encode()
        self.receiver_address.encode()
        self.payload.encode()
    
    def decode_payload(self):
        self.sender_address.decode()
        self.receiver_address.decode()
        self.payload.decode()