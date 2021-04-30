#!/usr/bin/python

import logging


from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server
from X32 import X32
from ActionParser import ActionParser

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

console = X32("10.192.97.134")
action_parser = ActionParser(console)

def handle_default(address, *args):
    logging.info(f" Passing command with address \"{address}\" to X32")
    # console.send_message(address, args)

def handle_simple_osc(address, *args):
    for arg in args:
        action_parser.parse(arg)

def main():
    disp = dispatcher.Dispatcher()
    disp.set_default_handler(handle_default)
    disp.map("/SOSC", handle_simple_osc)

    server = osc_server.ThreadingOSCUDPServer(("127.0.0.1", 10023), disp)

    server.serve_forever()

if __name__ == "__main__":
    main()