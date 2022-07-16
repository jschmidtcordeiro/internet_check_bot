import unittest
import main

class TestPing(unittest.TestCase):

    def setUp(self):
        print("Setup")
        self.hosts_list = ["ufsc.br", "google.com", "spotify.com"]


    def test_ping(self):
        for host in self.hosts_list:
            # Test ping to hosts in hosts_list 
            response = main.ping(host)
            self.assertIs(type(response), str) 
            self.assertIn(f"PING {host}", response)

if __name__ == '__main__':
    unittest.main()
