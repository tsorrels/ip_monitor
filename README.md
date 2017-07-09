# IP_monitor

This project is a simple terminal IP traffic monitoring tool with simple a user interface and extensibility. No external dependencies.

To run in Linux (must be root):

```bash
$ sudo ./ip_monitor -i interface [-p] [Extention, ...]

```
The user must provide an interface (i.e. 'eth0'), can optionally provide the -p switch to run in permiscuous mode, and can concatenate any number of properly written extention modules that the tool will load prior to running.

A execution example would be:
```bash
$ sudo ./ip_monitor -i eth0 -p ip_time ip_whois ip_throttle
```


Strike 'arrow-up' and 'arrow-down' to scroll through connections. Strike 'r' to remove a connection from the state.  


## Extentions
### Model

Extending the tool is easy.  Write a module that that globally defines an Extension object named 'extension', defined in ip_extension.py. Load the modules by concatenating them only the executing command.

```python
class Extension(object):
    # must explicitly set all components; any can be an empty list
    def __init__(self, threads, hdr_extensions, data_extensions, cmd_extensions):
        self.threads = threads				# must be list
        self.header_extensions = hdr_extensions		# must be list
        self.data_extensions = data_extensions		# must be list
        self.cmd_extensions = cmd_extensions		# must be list
```


The model is a collection of 'connection' objects, defined in ip_connection.py. You can extend the model be defining a list of strings that the engine will add to the ip_connection objects as fields and make accessable.

```python
data_extensions = [ 'average_bps', ]

```

### View

The view is a series of columns with a defined string header and a matching field in the connection objects that the view will access when writing the display.

```python

class HeaderItem(object):
    def __init__(self, text, length, offset = None):
        self.text = text	# must be string
        self.length = length	# integer representing max character output for item
        self.offset = offset	# not used

```

![UI View](/terminal_view.jpeg)

The UI identifies the 'current' connection with underline. Strike the up or down key to scroll and select a differrent connection. Commands executed will operate on the current connection. 

Connections that have not experienced data transfer in the last 10 seconds are displayed in grey text. 


### Controller

The control can be extended by adding CmdExtension objects, defined in cmd_extension.py. The CmdExtension object simply defines an input key and a function to execute when pressed.  The programmer must take care to not allow a collision between input keys; each key may be mapped only once throughout the entire program.


```python
class CmdExtension(object):
    def __init__(self, key, function):
        self.key = key			# must be character
        self.function = function	# must be function definition

```

The function must have signature

### Current extensions
ip_time

ip_whois

ip_throttle

### Extension Example Definition

A very simple example of an extension follows.  This module extends the model and the view, but does not extend the controller.  Notice the final line which defines the global variable 'extension'.

```python
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

extension = Extension(Threads, Header_Extensions, Data_Extensions, [])
```

### Locking

### Logging mechanism


### Future ideas for extensions
Man in the Middle Module
Counter traffic module
Module to send SIGKILL to processes from this tool
Whitelist module, where only filtered traffic
