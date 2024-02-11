import unittest
import docker
import server


class TestServer(unittest.TestCase):

    def setUp(self):
        self.client = docker.from_env()

    def testSocketGenerated(self):
        # main_server = server.Server()
        # main_server.run_server_forever(server.HOST, server.PORT, 1)


if __name__=='__main__':
    unittest.main()