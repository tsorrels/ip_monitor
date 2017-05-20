import socket
import struct
from ctypes import *

class IP(Structure):
    _fields_ = [
        ("ihl", c_ubyte),
        #("version", c_ubyte, 4),
        ("tos", c_ubyte),
        ("raw_length", c_uint16),
        ("id", c_uint16),
        #("len", c_ushort),
        #("id", c_ushort),
        ("offset", c_uint16),
        #("offset", c_ushort),
        ("ttl", c_ubyte),
        ("protocol_num", c_ubyte),
        #("sum", c_uint16),
        #("sum", c_ushort),
        ("src", c_uint32),
        ("dst", c_uint32)
        ]


    def __new__(self, socket_buffer = None):
        return self.from_buffer_copy(socket_buffer)
     
    def __init__(self, socket_buffer = None):
        self.protocol_map = {1 : "ICMP", 6: "TCP", 17 : "UDP"}
        self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))
        self.length = socket.htons(self.raw_length)
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)
