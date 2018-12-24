from tcp_header import TCPHeader
from udp_header import UDPHeader

class TransportParser():
    def __init__(self):
        pass

    def parse_header(self, raw_buffer, protocol):
        if protocol == 'TCP':
            # check length
            return TCPHeader(raw_buffer)

        elif protocol == 'UDP':
            # check length
            return UDPHeader(raw_buffer)

        else:
            return None
        
