
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



class Display(object):
    def __init__(self):

        self.num_header_rows = 1 # TODO: replace this magic number
        self.cur_row = 1
        self.num_output_rows = 0
        self.stdscr = curses.initscr()
        self.stdscr.keypad(1)
        self.stdscr.nodelay(1)
        self.scr_dimmesions = self.stdscr.getmaxyx() # returns (height, width)

        curses.curs_set(0)
        curses.noecho()
        curses.halfdelay(5) # set input timeout for 5 tenths of a second
        #curses.cbreak()                        


    def __write_header(self):
        y = 0       # y-th line of terminal
        x = 0

        for header in self.state.display_headers:
            if (x + header.length) < self.scr_dimmesions[1]:
                self.stdscr.addnstr(y, x, header.text, header.length)
                x = x + header.length + 2


    
    def __write_line(self, y, connection, time):

        # indent 0 space
        x = 0
        attr = curses.A_DIM
        
        connection.RX = ''
        
        if (time - connection.time_last) < 1:
            attr = curses.A_BOLD
            connection.RX = '->'
            self.stdscr.addnstr(y, 15, "->", 4, attr)

        elif (time - connection.time_last) < 15:
            attr = curses.A_NORMAL

        if y == self.cur_row:
            attr = attr | curses.A_UNDERLINE

            
        for index in range (0, len(connection.attr_names)):
            # check if there is data to show for this attribute
            # and there is enough room on screen to display

            if getattr(connection, connection.attr_names[index]) and \
               (x + self.state.display_headers[index].length)< self.scr_dimmesions[1]:
                self.stdscr.addnstr(y, x,
                    str(getattr(connection, connection.attr_names[index])),
                    self.state.display_headers[index].length, attr)
            x = x + self.state.display_headers[index].length + 2

        
        
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
        y = self.num_header_rows

        # these functions use the counter and return the updated value
        y = self.__display_helper(y, self.state.tcp_connections, self.state.tcp_lock)
        y = self.__display_helper(y, self.state.udp_connections, self.state.udp_lock)
        y = self.__display_helper(y, self.state.icmp_connections, self.state.icmp_lock)

        self.num_output_rows = y - self.num_header_rows
        self.stdscr.refresh()


    def run(self):
        while True:
            ch = self.stdscr.getch()
            if ch != -1:
                cur_line = self.stdscr.instr(self.cur_row, 0)
                self.controller.do_operation(ch, cur_line)
            self.state.logwriter.write('error', str(ch))
            #if ch == curses.KEY_RESIZE:
            #    self.update_window()

            #else:
            #time.sleep(.5)
            self.display()
                
    def update_window(self):
        pass
        #self.stdscr = curses.initscr()
        #self.stdscr.keypad(1)
        self.scr_dimmesions = self.stdscr.getmaxyx() # returns (height, width)

        #self.scr_dimmesions = self.stdscr.getmaxyx()
        #self.display()
        #self.state.logwriter.write('error', str(self.scr_dimmesions))
        self.state.logwriter.write('error', str(self.stdscr.getmaxyx()))
