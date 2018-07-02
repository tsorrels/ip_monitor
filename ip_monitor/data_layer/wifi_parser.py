from link_parser import LinkLayerParser
from rt_header import RadiotapHeader
from w_header import WirelessHeader
from wifi_header import WifiHeader
from llc_header import LlcHeader

class WifiParser(LinkLayerParser):
    def __init__ (self):
        pass

    
    def parse_header(self, raw_buffer):
        rt_header = RadiotapHeader(raw_buffer)
        w_header = WirelessHeader(raw_buffer[rt_header.length:])
        llc_header = LlcHeader(raw_buffer[rt_header.length + w_header.length:])
        wifi_header = WifiHeader(rt_header, w_header, llc_header)
        
        return wifi_header
