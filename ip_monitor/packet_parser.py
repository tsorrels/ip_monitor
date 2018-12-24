from ip_layer.ip_parser import IPParser
from transport_layer.transport_parser import TransportParser
from packet import Packet


class PacketParser():
    def __init__(self, link_layer_parser):
        self.link_layer_parser = link_layer_parser
        self.ip_parser = IPParser()
        self.transport_parser = TransportParser()
        

    def parse_packet(self, raw_buffer):
        packet = Packet()
        
        link_layer_header = self.link_layer_parser.parse_header(raw_buffer)

        if not link_layer_header:
            return packet
            
        if not link_layer_header.is_parsable():
            return packet

        packet.set_link_header(link_layer_header)
        
        payload = raw_buffer[link_layer_header.length:]
        
        ip_header = self.ip_parser.parse_header(payload)

        if not ip_header:
            return packet

        packet.set_ip_header(ip_header)

        proto = ip_header.protocol

        #print ip_header.length
        #print ip_header.total_length
        
        
        payload = payload[ip_header.length:]

        #transport_header = self.transport_parser.parse_header(payload, proto)
	transport_header = None 

        if not transport_header:
            return packet

        packet.set_transport_header(transport_header)

        return packet
