

class WifiHeader(object):
    def __init__(self, rt_header, w_header):
        self.rt_header = rt_header
        self.w_header = w_header
        self.length = rt_header.length + w_header.length

    
    def is_parsable(self):
        if (self.w_header.frame_type == 'Data'
            and self.w_header.subtype != 'NullData'
            and self.w_header.subtype != 'NullQoS'
            and not self.w_header.protected):

            return True

        return False
