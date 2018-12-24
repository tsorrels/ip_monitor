from link_parser import LinkLayerParser
from eth_header import EthHeader
from eth_header import header_size

class EthParser(LinkLayerParser):
    def __init__(self):
        pass
        #self.header_size = 14

    def parse_header(self, raw_buffer):
        if len(raw_buffer) < header_size:
            return None

        return EthHeader(raw_buffer[0:header_size])
