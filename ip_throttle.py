import time
import subprocess
from display_headers import HeaderItem
from ip_extension import Extension
from ip_command import IPCommand

STATUS_NONE = None
STATUS_THROTTLED = "Throttled"
STATUS_SET_RELEASE = "Releasing"
STATUS_RELEASED = "Released"


DEL_QDISC_STRING = 'tc qdisc del dev {0} ingress'

ADD_QDISC_STRING = 'tc qdisc add dev {0} handle ffff: ingress'
 
ADD_FILTER_STRING = 'tc filter add dev {0} parent ffff: \
    protocol ip prio {1} \
    u32 match ip src {2} \
    police rate 1kbit buffer 1k drop \
    flowid :1'

DEL_FILTER_STRING = 'tc filter del dev {0} parent ffff: prio {1}'

LOG_HANDLE = "log_file_handle"

filter_map = {}

cur_prio = 20

def Run(state):

    # add log to state
    state.logwriter.add_log(LOG_HANDLE, 'throttle_log.txt')
    
    try:
        # remove ingress qdisc
        subprocess.call(DEL_QDISC_STRING.format(state.interface), shell=True)

    except CalledProcessError as E:
        # throws error if no ingress qdisc is installed
        pass
        
    # install ingress qdisc
    subprocess.call(ADD_QDISC_STRING.format(state.interface), shell=True )

    try:
        while True:
            time.sleep(1)
            with state.all_lock:
                for connection in state.all_connections:
                    if  connection.throttle_status == STATUS_NONE:
                        throttle_connection(connection, state)

                    elif connection.throttle_status == STATUS_THROTTLED:
                        pass

                    elif connection.throttle_status == STATUS_SET_RELEASE:
                        remove_throttle(connection, state)

                    elif connection.throttle_status == STATUS_RELEASED:
                        pass

                    else:
                        # error
                        pass

    except Exception as e:
        state.logwriter.write(LOG_HANDLE, str(e))

def remove_throttle(connection, state):
    prio = filter_map[connection.src_address]
    subprocess.call(DEL_FILTER_STRING.format(state.interface, prio), shell=True)
    connection.throttle_status = STATUS_RELEASED
    

def throttle_connection(connection, state):
    global cur_prio
    cmd_string = ADD_FILTER_STRING.format(state.interface,
                                          str(cur_prio),
                                          connection.src_address)
    subprocess.call(cmd_string, shell=True)
    filter_map[connection.src_address] = cur_prio    
    cur_prio = cur_prio + 1
    connection.throttle_status = STATUS_THROTTLED


def toggle_throttled(data, state):
    connection = state.find_connection(data)
    with state.all_lock:
        if connection.throttle_status == STATUS_THROTTLED:
            remove_throttle(connection, state)

        elif connection.throttle_status == STATUS_RELEASED:
            throttle_connection(connection, state)

        else:
            # error
            pass
        

Threads = [Run, ]
Header_Extensions = [HeaderItem('Throttle', 10)]
Data_Extensions = [ 'throttle_status', ]
Cmd_Extensions = [ IPCommand('t', toggle_throttled), ]

extension = Extension(Threads, Header_Extensions, Data_Extensions, Cmd_Extensions)
