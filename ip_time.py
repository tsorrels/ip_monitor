import socket
import time
from cmd_extension import CmdExtension
from display_headers import HeaderItem
from ip_extension import Extension

def format_time(time):
    returnString = ''
    if time < 60:
        returnString = str(int(time)) + 's'

    elif time < 60 * 60:
        returnString = str(int(time) / 60) + 'm'

    else:
        returnString = str(max(99, int(time) / 60 / 60)) + 'h'
            
    return returnString


def refresh_time(data, state):
    connection = state.find_connection(data)
    now = time.time() - 1
    with state.all_lock:
        connection.time_last = now


def run_time(state):
    connections = state.all_connections
    lock = state.all_lock
    
    now = time.time()
    with lock:
        for connection in connections:
            connection.time_elapsed = format_time(now - connection.time_last)
    
    
def Run(state):
    while True:
        run_time(state)
        time.sleep(1)
    

Threads = [Run,]
Header_Extensions = [ HeaderItem('Time', 4), ]
Data_Extensions = [ 'time_elapsed', ]
Cmd_Extensions = [ CmdExtension('R', refresh_time),]

extension = Extension(Threads, Header_Extensions, Data_Extensions, Cmd_Extensions)
