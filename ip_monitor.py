#!/usr/bin/env python2

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

# from optparse import OptionParser


class GlobalState(object):
    def __init__(self, mods):
        self.stdscr = curses.initscr()
        self.stdscr.keypad(1)
        self.scr_dimmesions = self.stdscr.getmaxyx() # returns (height, width)

        self.logwriter = LogWriter()
        self.logwriter.add_log('error', './error_log.txt')        
        
        self.udp_connections = []
        self.udp_lock = threading.Lock()
        self.tcp_connections = []
        self.tcp_lock = threading.Lock()
        self.icmp_connections = []
        self.icmp_lock = threading.Lock()

        self.header_extensions = []
        self.data_extensions = []
        self.run_threads = []
        
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()                        

        self.display_headers = default_headers

        for mod in mods:
            self.__load_mod(mod)


    def __load_mod(self, mod):
        try:
            importlib.import_module(mod)

            #add headers
            for header in sys.modules[str(mod)].Header_Extensions:
                #self.header_extensions.append(header)
                self.display_headers.append(header)
                
            #add connection data
            for data in sys.modules[str(mod)].Data_Extensions:
                self.data_extensions.append(data)
            
            #add execution threads             
            for runnable in sys.modules[str(mod)].Threads:
                self.run_threads.append(runnable)
        
            
        except KeyError as e:
            self.logwriter.write('error', "Key error")
            
        
        except Exception as e:
            self.logwriter.write('error', 'Other exception, ' + mod + str(e))



    def __write_header(self):
        y = 0       # y-th line of terminal
        offset = 0

        for header in self.display_headers:
            self.stdscr.addnstr(y, offset, header.text, header.length)
            offset = offset + header.length + 2


    def __format_time(self, time):
        returnString = ''
        if time < 60:
            returnString = str(int(time)) + 's'

        elif time < 60 * 60:
            returnString = str(int(time) / 60) + 'm'

        else:
            returnString = str(max(99, int(time) / 60 / 60)) + 'h'

            
        return returnString
            
    def __write_line(self, y, connection, time):

        # indent 0 space
        x = 0
        attr = curses.A_DIM

        connection.RX = ''
        
        if (time - connection.time_last) < 1:
            attr = curses.A_BOLD
            #offset = display_offsets["RX"]
            connection.RX = '->'
            self.stdscr.addnstr(y, 15, "->", 4, attr)

        elif (time - connection.time_last) < 15:
            attr = curses.A_NORMAL
        
        for index in range (0, len(connection.attr_names)):
            self.stdscr.addnstr(y, x,
                    str(getattr(connection, connection.attr_names[index])),
                    self.display_headers[index].length, attr)
            x = x + self.display_headers[index].length + 2

        
        
    def __display_helper(self, counter, connections, lock):
        now = time.time()
        with lock:
            for connection in connections:
                self.__write_line(counter, connection, now)
                counter = counter + 1

        return counter

        

    def display(self):
        self.stdscr.clear()
        self.__write_header()
        y = 1

        # these functions use the counter and return the updated value
        y = self.__display_helper(y, self.tcp_connections, self.tcp_lock)
        y = self.__display_helper(y, self.udp_connections, self.udp_lock)
        y = self.__display_helper(y, self.icmp_connections, self.icmp_lock)

                                        
        self.stdscr.refresh()

def runWhois(state):
    connectionTuples = []
    connectionTuples.append( (state.udp_connections, state.udp_lock) ) 
    connectionTuples.append( (state.tcp_connections, state.tcp_lock) )
    connectionTuples.append( (state.icmp_connections, state.icmp_lock) )

    whoisClient = WHOISClient(connectionTuples)
    whoisClient.run()
        

def sniff(protocol, connections, lock, file_handle = None, file_lock = None):

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, protocol)
    sniffer.bind(("0.0.0.0", 0))
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    try:        
        while True:

            raw_buffer = sniffer.recvfrom(65565)[0]        
            ip_header = IP(raw_buffer[0:20])
        
            #print "Protocol: %s %s -> %s" % (ip_header.protocol, \
                                    # ip_header.src_address, \
                                     #     ip_header.dst_address)

            newConnection = True
            new_time = time.time()
            with lock:
                for connection in connections:
                    if ip_header.src == connection.src and \
                    ip_header.dst == connection.dst:
                        # update connection
                        connection.data += ip_header.len
                        connection.time_last = new_time
                        connection.RX = True
                        newConnection = False

                        # update display
                        
                        break

            if newConnection:
            # append is thread safe
            # this is the only thread writing to this list
                connections.append(IPConnection(ip_header, new_time))
                if file_lock and file_handle:
                    with file_lock:
                        file_handle.write('Added new connection\n')
                
                
    except Exception as e:
        if file_handle and file_lock:
            with file_lock:
                file_handle.write(str(e) + '\n')
                traceback.print_exc(limit=None, file=file_handle)


def SIGINT_handler(signal, frame):
    curses.endwin()
    exit(0)
            
def import_modules(mods):
    for mod in mods:
        importlib.import_module(mod)

    
    
def main():

    
    error_file = open("./error_log.txt", "a")
    file_lock = threading.Lock()
    
    (optlist, args) = getopt.getopt(sys.argv[1:], 'p')

    import_modules(args)
    
    state = GlobalState(args)

    signal.signal(signal.SIGINT, SIGINT_handler)


    if os.name == "nt":
	print 'OS is "nt"'
        thread_win = threading.Thread(target = sniff,
                                   args = (socket.IPPROTO_IP,))
        while True:
            time.sleep(5)

        return

    # else
    thread_icmp = threading.Thread(target = sniff,
                                   args = (socket.IPPROTO_ICMP,
                                           state.icmp_connections, 
                                           state.icmp_lock,
                                           error_file,
                                           file_lock))
    thread_tcp = threading.Thread(target = sniff,
                                   args = (socket.IPPROTO_TCP,
                                           state.tcp_connections,
                                           state.icmp_lock,
                                           error_file,
                                           file_lock))
    thread_udp = threading.Thread(target = sniff,
                                   args = (socket.IPPROTO_UDP,
                                           state.udp_connections,
                                           state.icmp_lock,
                                           error_file,
                                           file_lock))
    #thread_whois = threading.Thread(target = runWhois, args = (state,))

    thread_icmp.daemon = True
    thread_tcp.daemon = True
    thread_udp.daemon = True
    #thread_whois.daemon = True
    
    thread_icmp.start()
    thread_tcp.start()
    thread_udp.start()

    for run in state.run_threads:
        thread = threading.Thread(target = run, args = (state, ))
        thread.daemon = True
        thread.start()
                                  
    #thread_whois.start()

    
    while True:
        time.sleep(.5)
        state.display()
    

if __name__ == "__main__":

    main()
