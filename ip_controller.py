import curses



class Controller(object):
    def __init__(self, display, state):

        self.__operations = { }        
        self.__populate_core_operations()
        self.display = display
        self.state = state
        self.__map_extensions()

    def __populate_core_operations(self):

        self.__operations[ord('r')] = self.__remove
        self.__operations[ord('p')] = self.__toggle_pause
        self.__operations[curses.KEY_UP] = self.__move_up
        self.__operations[curses.KEY_DOWN] = self.__move_down
                       

    def __map_extensions(self):

        for cmd in self.state.cmd_extensions:
            if cmd.key in self.__operations:
                #TODO: return error, key can only be mapped once
                continue
            
            self.__operations[ord(cmd.key)] = cmd.function

        

    def do_operation(self, input, data):
        # edge case where data is an empty row
        # can result when user removes bottom connection
        if not data:
            pass
        try:
            self.__operations[input](data, self.state)

        except KeyError as e:
            self.state.logwriter.write('error', 'invalid input:' + str(input)
                                       +'\n')
            # TODO: return false to identify bad input
            pass


    def __move_up(self, data, state):
        if self.display.cur_row  > self.display.num_header_rows:
            self.display.cur_row -= 1
            self.display.display()

    def __move_down(self, data, state):
        if self.display.cur_row < self.display.num_output_rows + \
           self.display.num_header_rows - 1:
            self.display.cur_row += 1
            self.display.display()

        
    def __toggle_pause(self, data, state):
        pass

    def __remove(self, data, state):
        self.state.logwriter.write('error', 'ran __remove\n')
        connection = self.state.find_connection(data)
        if connection:
            with self.state.all_lock:
                self.state.all_connections.remove(connection)

                    
