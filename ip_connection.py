import time

class IPConnection(object):
    def __init__(self, ipHeader, time, attr_names = None):
        self.src = ipHeader.src
        self.dst = ipHeader.dst
        self.proto = ipHeader.protocol
        self.src_address = ipHeader.src_address
        self.dst_address = ipHeader.dst_address
        self.src_whois = ''
        self.dst_whois = ''
        self.time_begin = time
        self.time_last = time
        self.data = ipHeader.len
        self.state = None
        self.RX = True

	#self.data = []
	self.display = []
        self.attr_names = []

	#self.__populate_data()

        for attr in self.attr_names:
            setattr(self, attr, None)

        self.__populate_attrs()
            
    def __populate_attrs(self):
        self.attr_names.append('src_address')
        self.attr_names.append('RX')
        self.attr_names.append('dst_address')
        self.attr_names.append('proto')
        self.attr_names.append('data')
        
#    def __populate_data(self):
#	self.display.append( display_item(self.src_address) )
#       self.display.append( display_item("->") )
#	self.display.append( display_item(self.dst_address) )
#	self.display.append( display_item(self.proto) )
#	#self.data.display("TIME")
#	self.display.append( display_item(self.data) )
