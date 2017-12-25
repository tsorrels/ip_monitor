import unittest

from ip_monitor.wifi_parser import WifiParser

class TestWifiParser(unittest.TestCase):
    def setup(self):
	self.wifi_parser = WifiParser()

    def test_1(self):
	self.assertTrue(True)
