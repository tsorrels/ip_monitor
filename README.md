# IP_monitor

This project is a simple terminal IP traffic monitoring tool with simple user interface and extensibility.

To run Linux (must be root):

'''bash
$ sudo ./ip_monitor -i interface [-p] [Extention, ...]

'''
The user must provide an interface (i.e. 'eth0'), can optionally provide the -p switch to run in permiscuous mode, and can concatinate any number of properly written extention modules that the tool will load prior to running.

A execution example would be:
'''bash
$ sudo ./ip_monitor -i eth0 -p ip_time ip_whois ip_throttle
'''


Strike 'arrow-up' and 'arrow-down' to scroll through connections. Strike 'r' to remove a connection from the state.


##Extentions
###Model

Extending the tool is easy.  Write a module that that globally defines an Extension object named 'extension', defined in ip_extension.py. Load the modules by concatenating them only the executing command.

'''python
class Extension(object):
    # must explicitly set all components; any can be an empty list
    def __init__(self, threads, hdr_extensions, data_extensions, cmd_extensions):
        self.threads = threads				# must be list
        self.header_extensions = hdr_extensions		# must be list
        self.data_extensions = data_extensions		# must be list
        self.cmd_extensions = cmd_extensions		# must be list
'''

'''python

'''


The model is a collection of 'connection' objects, defined in ip_connection.py. You can extend the model be defining a list of strings that the engine will add to the ip_connection objects as fields and make accessable.

'''python
data_extensions = [ 'average_bps', ]

'''



The view is a series of columns with a defined string header and a matching field in the connection objects that the view will access when writing the display.

'''python

class HeaderItem(object):
    def __init__(self, text, length, offset = None):
        self.text = text	# must be string
        self.length = length	# integer representing max character output for item
        self.offset = offset	# not used

'''


The control can be extended by adding CmdExtension objects, defined in cmd_extension.py. The CmdExtension object simply defines an input key and a function to execute when pressed.  The programmer must take care to not allow a collision between input keys; each key may be mapped only once throughout the entire program.


'''python
class CmdExtension(object):
    def __init__(self, key, function):
        self.key = key			# must be character
        self.function = function	# must be function definition

'''

No external dependenc
