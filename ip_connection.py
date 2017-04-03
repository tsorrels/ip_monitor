import time


class IPConnection(object):
    def __init__(self, ipHeader, time):
        self.src = ipHeader.src
	self.dst = ipHeader.dst
	self.proto = ipHeader.protocol
        self.src_address = ipHeader.src_address
	self.dst_address = ipHeader.dst_address
	self.src_whois = ''
	self.dst_whois = ''
	self.time_begin = time
	self.time_last = time
	self.data = ipHeader.len
	self.state = None
        self.RX = True
