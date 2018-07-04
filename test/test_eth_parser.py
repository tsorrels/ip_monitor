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
        expected_src_mac = '0c:8b:fd:75:a7:38'
        expected_dst_mac = '00:00:ca:11:22:33'
        
        eth_header = eth_parser.parse_header(hex_data)

        self.assertEqual(expected_src_mac, eth_header.src)
        self.assertEqual(expected_dst_mac, eth_header.dst)
