
class Packet():
    def __init__(self):
        self.application_headers = []
        self.link_header = None
        self.ip_header = None
        self.transport_header = None

    def set_link_header(self, header):
        self.link_header = header


    def set_ip_header(self, header):
        self.ip_header = header

    def set_transport_header(self, header):
        self.transport_header = header
