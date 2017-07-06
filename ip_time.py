
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

def run_time(state):
    #(connections, lock) = state.connections_map[protocol]
    connections = state.all_connections
    lock = state.all_lock
    
    now = time.time()
    with lock:
        for connection in connections:
            connection.time_elapsed = format_time(now - connection.time_last)
    
    

def Run(state):
    while True:
        run_time(state)
        #run_time(socket.IPPROTO_UDP, state)
        #run_time(socket.IPPROTO_TCP, state)
        #run_time(socket.IPPROTO_ICMP, state)
        time.sleep(1)
    

Threads = [Run,]

Header_Extensions = [ HeaderItem('Time', 4), ]

Data_Extensions = [ 'time_elapsed', ]
        
extension = Extension(Threads, Header_Extensions, Data_Extensions, [])
