import unittest
import time
from src.ssh_server import SshServer


class TestServer(unittest.TestCase):
    def test_server_start(self):
        server = SshServer('../config/id_rsa')
        server.start(port=2222)
        time.sleep(5)
        server.stop()
