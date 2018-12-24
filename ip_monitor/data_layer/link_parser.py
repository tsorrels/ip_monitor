from abc import ABCMeta


class LinkLayerParser(object):
    __metaclass__ = ABCMeta

    def __init__(self, state):
        self.header_size = None
        self.header_class = None

    def parse_header(self, buffer):
        pass
