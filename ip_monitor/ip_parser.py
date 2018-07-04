from ip_header import header_min_size
from ip_header import IPHeader

class IPParser():
    def __init__(self):
        pass

    def parse_header(self, raw_buffer):
        if len(raw_buffer) < header_min_size:
            return None

        return IPHeader(raw_buffer)
