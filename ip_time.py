
import socket
import time
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

def run_time(protocol, state):
    (connections, lock) = state.connections_map[protocol]

    now = time.time()
    with lock:
        for connection in connections:
            connection.time_elapsed = format_time(now - connection.time_last)
    
    

def Run(state):
    while True:
        run_time(socket.IPPROTO_UDP, state)
        run_time(socket.IPPROTO_TCP, state)
        run_time(socket.IPPROTO_ICMP, state)
        time.sleep(1)
    

Threads = [Run,]

Header_Extensions = [ HeaderItem('Time', 4), ]


Data_Extensions = [ 'time_elapsed', ]

        
extension = Extension()
extension.threads = Threads
extension.header_extensions = Header_Extensions
extension.data_extensions = Data_Extensions

