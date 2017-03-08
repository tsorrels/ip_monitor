
import threading
import os
import struct
import socket
import time
#from ctypes import *

from ip_header import IP



def sniff(protocol):

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, protocol)
    #sniffer.bind((socket.gethostbyname(socket.gethostname()), 0))
    sniffer.bind(("0.0.0.0", 0))
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        
    while True:

        raw_buffer = sniffer.recvfrom(65565)[0]
        
        ip_header = IP(raw_buffer[0:20])
        
        print "Protocol: %s %s -> %s" % (ip_header.protocol,
                                         ip_header.src_address,
                                         ip_header.dst_address)




def main():
    
    if os.name == "nt":
	print 'OS is "nt"'
        thread_win = threading.Thread(target = sniff,
                                   args = (socket.IPPROTO_IP,))
        while True:
            time.sleep(5)

        return

    # else
    thread_icmp = threading.Thread(target = sniff,
                                   args = (socket.IPPROTO_ICMP,))
    thread_tcp = threading.Thread(target = sniff,
                                   args = (socket.IPPROTO_TCP,))
    thread_udp = threading.Thread(target = sniff,
                                   args = (socket.IPPROTO_UDP,))

    thread_icmp.start()
    thread_tcp.start()
    thread_udp.start()
    
    print "Running"

    while True:
        time.sleep(5)
    



#except KeyboardInterrupt:

 #   if os.name == "nt":
  #      sniffer.ioctl(socket.SIO_RCVAL, socket.RCVALL_OFF)



if __name__ == "__main__":
    main()
