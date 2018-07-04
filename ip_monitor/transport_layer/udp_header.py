import socket
import struct
from ctypes import *

class UDPHeader(Structure):
    _fields_ = [
        ("src_port", c_uint16),
        ("dst_port", c_uint16),
        ("udp_length", c_uint16),
        ("checksum", c_uint16)
        ]


    def __new__(self, socket_buffer = None):
        return self.from_buffer_copy(socket_buffer)
     
    def __init__(self, socket_buffer = None):
        self.length = socket.htons(self.udp_length)
