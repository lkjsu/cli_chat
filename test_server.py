import unittest
from client import Client


class TestServer(unittest.TestCase):
    def setUp(self):
        self.host = '0.0.0.0'
        self.port = 3874
        self.client = Client()


if __name__=='__main__':
    unittest.main()