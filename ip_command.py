
class IPCommand(object):

    def __init__(self, cmd_character, target_function):

        self.key = cmd_character
        self.function = target_function
