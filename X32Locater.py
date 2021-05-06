from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server

import logging
import time

class X32Locater:
    def __init__(self, broadcast_address):
        self.disp = dispatcher.Dispatcher()
        self.disp.set_default_handler(print)
        self.server = osc_server.BlockingOSCUDPServer(("0.0.0.0", 10023), self.disp)
        self.client = udp_client.SimpleUDPClient(broadcast_address, 10023, allow_broadcast=True)
        self.server.socket = self.client._sock

    def locate(self):
        is_done = False
        ip = None
        def handle_response(ip_address, address, *args1):
            nonlocal is_done
            nonlocal ip
            logging.info(f" X32 found on ip address {ip_address[0]}.")
            is_done = True
            ip = ip_address[0]
        
        self.disp.map("/info", handle_response, needs_reply_address=True)
        last_send = time.time()
        while not is_done:
            self.server.handle_request()
            if(time.time()-last_send > 1.0):
                last_send = time.time()
                logging.info(" Searching for X32...")
                self.client.send_message("/info", [])

        self.disp.unmap("/info", handle_response, needs_reply_address=True)

        return ip