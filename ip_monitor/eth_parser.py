from link_parser import LinkLayerParser
from eth_header import EthHeader
from eth_header import header_size

class EthParser(LinkLayerParser):
    def __init__(self, state):
        self.header_size = 14

    def parse_header(self, buffer):
        return EthHeader(buffer[0:header_size])
