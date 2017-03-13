#!/usr/bin/env python2

import signal
import threading
import os
import struct
import socket
import time
import curses
from ip_connection import IPConnection
from ip_header import IP


# map encoding display offset descriptions for text UI
# first tuple element is horizontal offset, second is max length
display_offsets = {"SRCIP" : ( 0, 15) ,
                   "RX"    : (16,  4) ,
                   "DSTIP" : (21, 15) ,
                   "PROTO" : (37,  5) ,
                   "TIME"  : (45,  4) ,
                   "DATA"  : (51, 15) }


class GlobalState(object):
    def __init__(self):
        self.stdscr = curses.initscr()
        self.stdscr.keypad(1)
        self.scr_dimmesions = self.stdscr.getmaxyx() # returns (height, width)

        
        self.udp_connections = []
        self.udp_lock = threading.Lock()
        self.tcp_connections = []
        self.tcp_lock = threading.Lock()
        self.icmp_connections = []
        self.icmp_lock = threading.Lock()

        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()                        


    def __write_header(self):
        y = 0
        offset = display_offsets["SRCIP"]
        self.stdscr.addnstr(y, offset[0], "SOURCE IP", offset[1])

        offset = display_offsets["DSTIP"]
        self.stdscr.addnstr(y, offset[0], "DESTINATION IP", offset[1])

        offset = display_offsets["PROTO"]
        self.stdscr.addnstr(y, offset[0], "PROTOCOL", offset[1])

        offset = display_offsets["TIME"]
        self.stdscr.addnstr(y, offset[0], "TIME", offset[1])
        
        offset = display_offsets["DATA"]
        self.stdscr.addnstr(y, offset[0], "BYTES", offset[1])


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

        attr = curses.A_DIM

        if (time - connection.time_last) < 1:
            attr = curses.A_BOLD
            offset = display_offsets["RX"]
            self.stdscr.addnstr(y, offset[0]  + 1, "->", offset[1], attr)

        elif (time - connection.time_last) < 15:
            attr = curses.A_NORMAL
        
        offset = display_offsets["SRCIP"]
        self.stdscr.addnstr(y, offset[0]  + 1, connection.src_address, offset[1],
                            attr)


        offset = display_offsets["DSTIP"]
        self.stdscr.addnstr(y, offset[0] + 1, connection.dst_address, offset[1],
                            attr)

        offset = display_offsets["PROTO"]
        self.stdscr.addnstr(y, offset[0] + 1, connection.proto, offset[1], attr)


        offset = display_offsets["TIME"]
        self.stdscr.addnstr(y, offset[0] + 1, self.__format_time(
            time - connection.time_last), offset[1], attr)

        
        offset = display_offsets["DATA"]
        self.stdscr.addnstr(y, offset[0] + 1, str(connection.data), offset[1], attr)

        
        
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
        
        

def sniff(protocol, connections, lock):

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, protocol)
    sniffer.bind(("0.0.0.0", 0))
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        
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
                    break

        if newConnection:
            # append is thread safe
            # this is the only thread writing to this list
            connections.append(IPConnection(ip_header, new_time))
                                


def SIGINT_handler(signal, frame):
    curses.endwin()
    exit(0)
            

def main():

    state = GlobalState()

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
                                           state.icmp_lock))
    thread_tcp = threading.Thread(target = sniff,
                                   args = (socket.IPPROTO_TCP,
                                           state.tcp_connections,
                                           state.tcp_lock))
    thread_udp = threading.Thread(target = sniff,
                                   args = (socket.IPPROTO_UDP,
                                           state.udp_connections,
                                           state.udp_lock))

    thread_icmp.daemon = True
    thread_tcp.daemon = True
    thread_udp.daemon = True

    
    thread_icmp.start()
    thread_tcp.start()
    thread_udp.start()

    

    
    while True:
        time.sleep(.5)
        state.display()
    



if __name__ == "__main__":
    main()
