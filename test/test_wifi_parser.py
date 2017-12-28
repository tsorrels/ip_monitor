import unittest

from ip_monitor.wifi_parser import WifiParser

class TestWifiParser(unittest.TestCase):
    def setup(self):
	self.wifi_parser = WifiParser()

    def test_1(self):
	self.assertTrue(True)

    def test_wifi_header_parsed(self):
        wifi_parser = WifiParser()
        
        fd = open('./test/test_data/wifi_frame_tcp_hex_string.txt')
        hex_string = fd.read()
        hex_string = hex_string.strip() #remove whitespace from string
        hex_data = (str(hex_string)).decode('hex')
        expected_src_mac = '00:08:ca:f7:72:ca'
        expected_dst_mac = 'f4:3e:9d:03:63:95'
        expected_bssid = '74:85:2a:4d:9c:aa'
        
        wifi_header = wifi_parser.parse_header(hex_data)

        self.assertEqual(expected_bssid, wifi_header.w_header.addr1) 
        self.assertEqual(expected_src_mac, wifi_header.w_header.addr2) 
        self.assertEqual(expected_dst_mac, wifi_header.w_header.addr3) 


    def test_wifi_header_encryted(self):
        wifi_parser = WifiParser()
        
        fd = open('./test/test_data/wifi_frame_encrypted_hex_string.txt')
        hex_string = fd.read()
        hex_string = hex_string.strip() #remove whitespace from string
        hex_data = (str(hex_string)).decode('hex')

        wifi_header = wifi_parser.parse_header(hex_data)

        self.assertEqual(1, wifi_header.w_header.protected)

    def test_wifi_header_not_encryted(self):
        wifi_parser = WifiParser()

        fd = open('./test/test_data/wifi_frame_tcp_hex_string.txt')        
        hex_string = fd.read()
        hex_string = hex_string.strip() #remove whitespace from string
        hex_data = (str(hex_string)).decode('hex')

        wifi_header = wifi_parser.parse_header(hex_data)

        self.assertEqual(0, wifi_header.w_header.protected)
        
