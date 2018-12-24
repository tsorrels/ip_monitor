import unittest

from ip_monitor.packet_parser import PacketParser
from ip_monitor.data_layer.eth_parser import EthParser

class TestPacketParser(unittest.TestCase):
    def setUp(self):
        link_parser = EthParser()
	self.packet_parser = PacketParser(link_parser)

    def test_eth_dns_packet_parsed(self):
        fd = open('./test/test_data/eth_frame_dns_hex_string.txt')
        hex_string = fd.read()
        hex_string = hex_string.strip() #remove whitespace from string
        hex_data = (str(hex_string)).decode('hex')
        expected_src_ip = '192.168.1.108'
        expected_dst_ip = '192.168.1.1'
        
        packet = self.packet_parser.parse_packet(hex_data)

        self.assertEqual(expected_src_ip, packet.ip_header.src_address) 
        self.assertEqual(expected_dst_ip, packet.ip_header.dst_address) 
        self.assertEqual('UDP', packet.ip_header.protocol)
        self.assertEqual(60, packet.ip_header.total_length)

        self.assertEqual(46321, packet.transport_header.src_port)
        self.assertEqual(53, packet.transport_header.dst_port)
        self.assertEqual(40, packet.transport_header.total_length)


    def test_eth_tcp_syn_packet(self):
        fd = open('./test/test_data/HTTP/tcp_syn_packet_hex.txt')
        hex_string = fd.read()
        hex_string = hex_string.strip() #remove whitespace from string
        hex_data = (str(hex_string)).decode('hex')

        packet = self.packet_parser.parse_packet(hex_data)

        print packet.transport_header.flags_raw
        print packet.transport_header.length
        
        self.assertEqual(59882, packet.transport_header.src_port)
        self.assertEqual(80, packet.transport_header.dst_port)
        self.assertEqual(1, packet.transport_header.syn)
