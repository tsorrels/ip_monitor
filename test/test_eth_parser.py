import unittest

from ip_monitor.data_layer.eth_parser import EthParser

class TestEthParser(unittest.TestCase):
    def setup(self):
        pass

    def test_1(self):
        self.assertTrue(True)

    def test_ethernet_header_parsed(self):
        eth_parser = EthParser()
        
        fd = open('./test/test_data/eth_frame_dns_hex_string.txt')
        hex_string = fd.read()
        hex_string = hex_string.strip() #remove whitespace from string
        hex_data = (str(hex_string)).decode('hex')
        expected_src_mac = '70:88:6b:83:75:03'
        expected_dst_mac = '00:21:29:b6:d8:a6'
        
        eth_header = eth_parser.parse_header(hex_data)

        self.assertEqual(expected_src_mac, eth_header.src)
        self.assertEqual(expected_dst_mac, eth_header.dst)
