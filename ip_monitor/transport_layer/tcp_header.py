import socket
import struct
from ctypes import *

class TCPHeader(Structure):
    _fields_ = [
        ("src_port", c_uint16),
        ("dst_port", c_uint16),
        ("seqnum", c_uint32),
        ("acknum", c_uint32),
        ("data_offset", c_uint16, 4),
        ("res", c_uint16, 6),
        ("flags", c_uint16, 6),
        ("window_size", c_uint16),
        ("checksum", c_uint16),
        ("urgent", c_uint16)
        ]


    def __new__(self, socket_buffer = None):
        return self.from_buffer_copy(socket_buffer)
     
    def __init__(self, socket_buffer = None):
        self.length = socket.htons(self.data_offset)
