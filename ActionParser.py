from X32 import X32
import logging

class ActionParser:
    def __init__(self, console: X32):
        self.__console = console

    def parse(self, action: str):
        if(action[0] == 'm'):
            paremeter = self.character_perameter(action)
            if(action[1] == 'c'):
                if(paremeter == 'm'):
                    self.__console.mute_channel(self.get_channel_number(action))
                if(paremeter == 'l'):
                    self.__console.unmute_channel(self.get_channel_number(action))
            if(action[1] == 'a'):
                if(paremeter == 'm'):
                    self.__console.mute_auxin(self.get_channel_number(action))
                if(paremeter == 'l'):
                    self.__console.unmute_auxin(self.get_channel_number(action))
            if(action[1] == 'b'):
                if(paremeter == 'm'):
                    self.__console.mute_bus(self.get_channel_number(action))
                if(paremeter == 'l'):
                    self.__console.unmute_bus(self.get_channel_number(action))
            if(action[1] == 'd'):  
                if(paremeter == 'm'):
                    self.__console.mute_dca(self.get_channel_number(action))
                if(paremeter == 'l'):
                    self.__console.unmute_dca(self.get_channel_number(action))
        
        elif(action[0] == 'f'):
            paremeter = self.float_peramerter(action)
            if(action[1] == 'c'):
                self.__console.set_channel_fader(self.get_channel_number(action), paremeter)
            if(action[1] == 'a'):
                self.__console.set_auxin_fader(self.get_channel_number(action), paremeter)
            if(action[1] == 'b'):
                self.__console.set_bus_fader(self.get_channel_number(action), paremeter)
            if(action[1] == 'd'):  
                self.__console.set_dca_fader(self.get_channel_number(action), paremeter)

        else:
            logging.warning(f" Unrecognized action charater '{action[0]}'")

    def get_channel_number(self, action: str):
        return int(action[2:].split(':')[0])

    def character_perameter(self, action: str):
        return action.split(':')[1]

    def float_peramerter(self, action: str):
        return float(action.split(':')[1])