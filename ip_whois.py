
import socket
import time
from ip_monitor.display_headers import HeaderItem
from ip_monitor.ip_extension import Extension

MAXRESPONSESIZE = 8192

HOST_STRING = "This host\n"

class WHOISClient(object):

    # connections is a list of tuples (list of connections, lock)
    def __init__(self, connectionTuples, state):
        self.connectionTuples = connectionTuples
        self.etcHosts = self.__readEtcHosts()
        self.state = state
        self.state.logwriter.add_log('whois', 'whoislog.txt')

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
        self.state.logwriter.write('whois', 'running\n')

        while True:
            try:

                time.sleep(2)
                # find connection with no resolution
                for connectionTuple in self.connectionTuples:
                    for connection in connectionTuple[0]:
                        if not connection.src_whois:
                            whois = self.__getWhois(connection.src_address)
                            if whois:
                                # recheck connection
                                if connectionTuple:
                                # acquire lock
                                    with connectionTuple[1]:
                                        connection.src_whois = whois
            except Exception, e:
                self.state.logwriter.write('whois', str(e) + '\n')
                    

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
                        self.state.logwriter.write('whois', words[1] + '\n')

                        return words[1]
        except Exception, e:
            self.state.logwriter.write('whois', str(e) + '\n')
        return None

    
    def __getWhois(self, address):
        # first check /etc/hosts
        name = self.__checkEtcHosts(address)
        if name:
            return name


        # now check if it is this host
        elif address == self.state.host_address:
            return HOST_STRING
        
        # call whois
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('199.71.0.46', 43))
        response = ''
        s.send('n + ' + address + '\n')
        recv_len = 1
        try:
            while recv_len:

                data = s.recv(MAXRESPONSESIZE)                                
                recv_len = len(data)
                response += data
                if len(response) > 4096:
                    break

        except Exception, e:
            self.state.logwriter.write('whois', str(e) + '\n')                                            
        return self.__parseWhois(response)


def Run(state):
    connectionTuples = []
    connectionTuples.append( (state.udp_connections, state.udp_lock) ) 
    connectionTuples.append( (state.all_connections, state.all_lock) ) 
    connectionTuples.append( (state.tcp_connections, state.tcp_lock) )
    connectionTuples.append( (state.icmp_connections, state.icmp_lock) )
    
    client = WHOISClient(connectionTuples, state)
    client.run()

extension = Extension([Run,], [ HeaderItem('WhoIs', 26), ], [ 'src_whois', ], [])
