import unittest

from ip_monitor.data_layer.wifi_parser import WifiParser
from ip_monitor.ip_header import IP

class TestWifiParser(unittest.TestCase):
    def setup(self):
	self.wifi_parser = WifiParser()

    def test_1(self):
	self.assertTrue(True)

    def test_wifi_frame_ip_header_parsed(self):
        wifi_parser = WifiParser()
        
        fd = open('./test/test_data/wifi_frame_tcp_hex_string.txt')
        hex_string = fd.read()
        hex_string = hex_string.strip() #remove whitespace from string
        hex_data = (str(hex_string)).decode('hex')
        expected_src_mac = '0c:8b:fd:75:a7:38'
        expected_dst_mac = '00:00:ca:11:22:33'

        wifi_header = wifi_parser.parse_header(hex_data)

        ip_header = IP(hex_data[wifi_header.length:])

        src_ip = '10.238.192.58'
        dst_ip = '93.184.215.92'

        self.assertEqual(src_ip, ip_header.src_address)
        self.assertEqual(dst_ip, ip_header.dst_address)
