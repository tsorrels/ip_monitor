
class HeaderItem(object):
    def __init__(self, text, length, offset = None):
        self.text = text
        self.length = length
        self.offset = offset


default_headers = [ HeaderItem("SRCIP", 13),
                    HeaderItem("RX", 4),
                    HeaderItem("DSTIP", 13),
                    HeaderItem("PROTO", 5),
                    HeaderItem("DATA", 8) ]

