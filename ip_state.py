
import importlib
import traceback
import signal
import threading
import os
import struct
import socket
import time
import curses
import getopt
import sys
from ip_connection import IPConnection
from ip_header import IP
from display_headers import *
from display_item import *
from logwriter import LogWriter

import socket
import fcntl
import struct


class GlobalState(object):
    def __init__(self, optlist, mods):

        self.logwriter = LogWriter()
        self.logwriter.add_log('error', './error_log.txt')        
        
	self.all_connections = []
	self.all_lock = threading.Lock()
        self.udp_connections = []
        self.udp_lock = threading.Lock()
        self.tcp_connections = []
        self.tcp_lock = threading.Lock()
        self.icmp_connections = []
        self.icmp_lock = threading.Lock()

        self.connections_map = {
            socket.IPPROTO_ICMP : (self.icmp_connections, self.icmp_lock),
            socket.IPPROTO_UDP : (self.udp_connections, self.udp_lock),
            socket.IPPROTO_TCP : (self.tcp_connections, self.tcp_lock) }

        self.cmd_extensions = []
        self.header_extensions = []
        self.data_extensions = []
        self.run_threads = []
        
        self.display_headers = default_headers

        self.permiscuous = False
        self.interface = None
        
        # parse options
        for o, a in optlist:
            if o == '-p':
                self.permiscuous = True

            elif o in ('-i', '--interface'):
                self.interface = a
                                
        # load modules
        for mod in mods:
            self.__load_mod(mod)

        self.host_address = self.__get_ip_address(self.interface)
            
            

    def __load_mod(self, mod):
        try:
            importlib.import_module(mod)
            extension = sys.modules[str(mod)].extension

            #add commands
            for cmd in extension.cmd_extensions:
                self.cmd_extensions.append(cmd)
            
            #add headers
            for header in extension.header_extensions:
                #self.header_extensions.append(header)
                self.display_headers.append(header)
                
            #add connection data
            for data in extension.data_extensions:
                self.data_extensions.append(data)
            
            #add execution threads             
            for runnable in extension.threads:
                self.run_threads.append(runnable)
        
            
        except KeyError as e:
            self.logwriter.write('error', "Key error")
            
        
        except Exception as e:
            self.logwriter.write('error', 'Other exception, ' + mod + str(e))


    # taken from
    # https://stackoverflow.com/questions/24196932/
    # how-can-i-get-the-ip-address-of-eth0-in-python
    def __get_ip_address(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])
