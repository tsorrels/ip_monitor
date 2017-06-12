
import socket
import time
from display_headers import HeaderItem
from ip_extension import Extension

MAXRESPONSESIZE = 8192

class WHOISClient(object):

    # connections is a list of tuples (list of connections, lock)
    def __init__(self, connectionTuples):
        self.connectionTuples = connectionTuples
        self.etcHosts = self.__readEtcHosts()
        self.logfile = open('./whoislog.txt', 'a')
        

    def __isIpv4(self, string):
        return True

    # well formed lines in /etc/hosts are in format of
    # {IP address} \t {resolver}
    def __parseEtcHostsLine(self, line):
        words = line.split()
        if words:
            # check if this is a comment
            if words[0] == '#':
                return None

            # check if malformed
            if len(words) < 2:
                return None

            # check if address is valid ipv4
            if not self.__isIpv4(words[0]):
                return None
            
            return (words[0], words[1])
            
            
        else:
            # this was only white space
            return None
            
            
    def __readEtcHosts(self):
        entries = []
        with open('/etc/hosts', 'r') as f:
            for line in f:
                entry = self.__parseEtcHostsLine(line)
                if entry:
                    entries.append(entry)
        
        
    def run(self):
        self.logfile.write('running\n')

        while True:
            try:

                time.sleep(2)
                # find connection with no resolution
                for connectionTuple in self.connectionTuples:
                    self.logfile.write('searching connection tuple\n')
                    for connection in connectionTuple[0]:
                        self.logfile.write('found connection, whois =\n' +
                                           str(connection.src_whois))
                        if not connection.src_whois:
                            whois = self.__getWhois(connection.src_address)
                            if whois:
                                # recheck connection
                                if connectionTuple:
                                # acquire lock
                                    with connectionTuple[1]:
                                        connection.src_whois = whois
            except Exception, e:
                self.logfile.write(str(e) + '\n')
                    

    def __checkEtcHosts(self, address):
        if not self.etcHosts:
            return None
        
        for entry in self.etcHosts:
            if entry[0] == address:
                return entry[1]

        return None

    
    def __parseWhois(self, response):
        try:
            lines = response.split('\n')
            for line in lines:
                if line:
                    if line[0] == '#':
                        pass
                    words = line.split(None, 1)
                    if words[0] == 'Organization:':
                        self.logfile.write(words[1])
                        self.logfile.flush()

                        return words[1]
        except Exception, e:
            self.logfile.write(str(e) + '\n')
            self.logfile.flush()
        return None

    
    def __getWhois(self, address):
        # first check /etc/hosts
        name = self.__checkEtcHosts(address)
        if name:
            return name

        # call whois
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('199.71.0.46', 43))
        response = ''
        s.send('n + ' + address + '\n')
        recv_len = 1
        try:
            while recv_len:
                self.logfile.write('about to receive \n')
                self.logfile.flush()

                #data = s.recv(MAXRESPONSESIZE)
                data = s.recv(4096)
                
                self.logfile.write('receive returned\n')
                self.logfile.flush()
                
                recv_len = len(data)
                response += data
                if len(response) > 4096:
                    break

        except Exception, e:
            self.logfile.write(str(e) + '\n')
            self.logfile.flush()
            
            

        #self.logfile.write(response + '\n')
        self.logfile.write("Finished calling whois\n")
        self.logfile.flush()
        #self.logfile.close()
        
        return self.__parseWhois(response)


def Run(state):
    connectionTuples = []
    connectionTuples.append( (state.udp_connections, state.udp_lock) ) 
    connectionTuples.append( (state.all_connections, state.all_lock) ) 
    connectionTuples.append( (state.tcp_connections, state.tcp_lock) )
    connectionTuples.append( (state.icmp_connections, state.icmp_lock) )
    
    client = WHOISClient(connectionTuples)
    client.run()

Threads = [Run,]

Header_Extensions = [ HeaderItem('WhoIs', 10), ]


Data_Extensions = [ 'src_whois', ]

extension = Extension()
extension.threads = [Run,]
extension.header_extensions =  [ HeaderItem('WhoIs', 26), ]
extension.data_extensions = [ 'src_whois', ]
