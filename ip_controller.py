import curses



class Controller(object):
    def __init__(self, display):

        self.__operations = { }        
        self.__populate_core_operations()
        self.display = display
        

    def __populate_core_operations(self):

        self.__operations['r'] = self.__remove
        self.__operations['p'] = self.__toggle_pause
        self.__operations[curses.KEY_UP] = self.__move_up
        self.__operations[curses.KEY_DOWN] = self.__move_down
                       
    

    def do_operation(self, input, data):
        try:
            self.__operations[input](data)

        except KeyError as e:
            # TODO: return false to identify bad input
            pass


    def __move_up(self, data):
        if self.display.cur_row  > self.display.num_header_rows:
            self.display.cur_row -= 1
            self.display.display()

    def __move_down(self, data):
        if self.display.cur_row < self.display.num_output_rows + \
           self.display.num_header_rows - 1:
            self.display.cur_row += 1
            self.display.display()

        
    def __toggle_pause(self, data):
        pass

    def __remove(self, data):
        pass
    

        
