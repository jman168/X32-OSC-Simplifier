#!/usr/bin/python

import logging


from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server
from X32 import X32

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

X32_client = udp_client.SimpleUDPClient("192.168.10.1", 10023)

def handle_default(address, *args):
    print(address, args)

def main():
    disp = dispatcher.Dispatcher()
    disp.set_default_handler(handle_default)

    server = osc_server.ThreadingOSCUDPServer(("127.0.0.1", 10023), disp)

    console = X32("127.0.0.1")
    
    console.mute_channel(1)
    console.unmute_channel(1)
    console.set_channel_fader(1, 0.5)
    
    console.mute_auxin(1)
    console.unmute_auxin(1)
    console.set_auxin_fader(1, 0.5)
    
    console.mute_bus(1)
    console.unmute_bus(1)
    console.set_bus_fader(1, 0.5)
    
    console.mute_dca(1)
    console.unmute_dca(1)
    console.set_dca_fader(1, 0.5)


    server.serve_forever()

if __name__ == "__main__":
    main()