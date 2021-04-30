import logging

from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server
from bitarray import bitarray


class X32:
    def __init__(self, address):
        self.disp = dispatcher.Dispatcher()
        self.server = osc_server.BlockingOSCUDPServer(("localhost", 10023), self.disp)
        self.client = udp_client.SimpleUDPClient(address, 10023)

    def send_message(self, address, *args):
        self.client.send_message(address, args)

    def get_peremeter(self, address):
        is_done = False
        results = ()
        def handle_response(address, *args):
            nonlocal is_done
            nonlocal results
            is_done = True
            results = args

        self.disp.map(address, handle_response)

        self.send_message(address)
        while not is_done:
            self.server.handle_request()

        self.disp.unmap(address, handle_response)

        return results

    def set_bit_map(self, decimal, bit, value):
        bit_map = bitarray(endian='little')
        bit_map.frombytes(int(decimal).to_bytes(1, 'little'))
        bit_map[bit-1] = value
        return bit_map.tobytes()[0]


    # Commands for channels
    def mute_channel(self, channel: int):
        if(channel>32):
            logging.warning("Cannot control channels greater than 32.")
            return
        self.send_message(f"/ch/{str(channel).zfill(2)}/mix/on", "OFF")
        logging.info(f" Muting channel {channel}")

    def unmute_channel(self, channel: int):
        if(channel>32):
            logging.warning("Cannot control channels greater than 32.")
            return
        self.send_message(f"/ch/{str(channel).zfill(2)}/mix/on", "ON")
        logging.info(f" Unmuting channel {channel}")

    def set_channel_fader(self, channel: int, value: float):
        if(channel>32):
            logging.warning("Cannot control channels greater than 32.")
            return
        self.send_message(f"/ch/{str(channel).zfill(2)}/mix/fader", value)
        logging.info(f" Setting channel {channel} fader to {value}")

    def add_channel_to_dca(self, channel: int, dca: int):
        if(channel>32 or dca>8):
            logging.warning("Cannot control channels greater than 32 or DCAs greater than 8.")
            return

        current_bit_map = int(self.get_peremeter(f"/ch/{str(channel).zfill(2)}/grp/dca")[0])
        new_bit_map = self.set_bit_map(current_bit_map, dca, True)
        self.send_message(f"/ch/{str(channel).zfill(2)}/grp/dca", new_bit_map)
        logging.info(f" Adding channel {channel} to DCA {dca}")

    def remove_channel_from_dca(self, channel: int, dca: int):
        if(channel>32 or dca>8):
            logging.warning("Cannot control channels greater than 32 or DCAs greater than 8.")
            return

        current_bit_map = int(self.get_peremeter(f"/ch/{str(channel).zfill(2)}/grp/dca")[0])
        new_bit_map = self.set_bit_map(current_bit_map, dca, False)
        self.send_message(f"/ch/{str(channel).zfill(2)}/grp/dca", new_bit_map)
        logging.info(f" Removing channel {channel} to DCA {dca}")

    def clear_channel_dcas(self, channel: int):
        if(channel>32):
            logging.warning("Cannot control channels greater than 32.")
            return

        self.send_message(f"/ch/{str(channel).zfill(2)}/grp/dca", 0)
        logging.info(f" Removing channel {channel} from all DCAs")


    # Commands for auxins
    def mute_auxin(self, auxin: int):
        if(auxin>8):
            logging.warning("Cannot control auxins greater than 8.")
            return
        self.send_message(f"/auxin/{str(auxin).zfill(2)}/mix/on", "OFF")
        logging.info(f" Muting auxin {auxin}")

    def unmute_auxin(self, auxin: int):
        if(auxin>8):
            logging.warning("Cannot control auxins greater than 8.")
            return
        self.send_message(f"/auxin/{str(auxin).zfill(2)}/mix/on", "ON")
        logging.info(f" Unmuting auxin {auxin}")

    def set_auxin_fader(self, auxin: int, value: float):
        if(auxin>8):
            logging.warning("Cannot control auxins greater than 8.")
            return
        self.send_message(f"/auxin/{str(auxin).zfill(2)}/mix/fader", value)
        logging.info(f" Setting auxin {auxin} fader to {value}")

    def add_auxin_to_dca(self, auxin: int, dca: int):
        if(auxin>8 or dca>8):
            logging.warning("Cannot control auxins greater than 8 or DCAs greater than 8.")
            return

        current_bit_map = int(self.get_peremeter(f"/auxin/{str(auxin).zfill(2)}/grp/dca")[0])
        new_bit_map = self.set_bit_map(current_bit_map, dca, True)
        self.send_message(f"/auxin/{str(auxin).zfill(2)}/grp/dca", new_bit_map)
        logging.info(f" Adding auxin {auxin} to DCA {dca}")

    def remove_auxin_from_dca(self, auxin: int, dca: int):
        if(auxin>8 or dca>8):
            logging.warning("Cannot control auxins greater than 8 or DCAs greater than 8.")
            return

        current_bit_map = int(self.get_peremeter(f"/auxin/{str(auxin).zfill(2)}/grp/dca")[0])
        new_bit_map = self.set_bit_map(current_bit_map, dca, False)
        self.send_message(f"/auxin/{str(auxin).zfill(2)}/grp/dca", new_bit_map)
        logging.info(f" Removing auxin {auxin} to DCA {dca}")

    def clear_auxin_dcas(self, auxin: int):
        if(auxin>8):
            logging.warning("Cannot control auxins greater than 8.")
            return

        self.send_message(f"/auxin/{str(auxin).zfill(2)}/grp/dca", 0)
        logging.info(f" Removing auxin {auxin} from all DCAs")


    # Commands for busses
    def mute_bus(self, bus: int):
        if(bus>16):
            logging.warning("Cannot control busses greater than 16.")
            return
        self.send_message(f"/bus/{str(bus).zfill(2)}/mix/on", "OFF")
        logging.info(f" Muting bus {bus}")

    def unmute_bus(self, bus: int):
        if(bus>16):
            logging.warning("Cannot control busses greater than 16.")
            return
        self.send_message(f"/bus/{str(bus).zfill(2)}/mix/on", "ON")
        logging.info(f" Unmuting bus {bus}")

    def set_bus_fader(self, bus: int, value: float):
        if(bus>16):
            logging.warning("Cannot control busses greater than 16.")
            return
        self.send_message(f"/bus/{str(bus).zfill(2)}/mix/fader", value)
        logging.info(f" Setting bus {bus} fader to {value}")

    def add_bus_to_dca(self, bus: int, dca: int):
        if(bus>16 or dca>8):
            logging.warning("Cannot control busses greater than 16 or DCAs greater than 8.")
            return

        current_bit_map = int(self.get_peremeter(f"/bus/{str(bus).zfill(2)}/grp/dca")[0])
        new_bit_map = self.set_bit_map(current_bit_map, dca, True)
        self.send_message(f"/bus/{str(bus).zfill(2)}/grp/dca", new_bit_map)
        logging.info(f" Adding bus {bus} to DCA {dca}")

    def remove_bus_from_dca(self, bus: int, dca: int):
        if(bus>16 or dca>8):
            logging.warning("Cannot control busses greater than 16 or DCAs greater than 8.")
            return

        current_bit_map = int(self.get_peremeter(f"/bus/{str(bus).zfill(2)}/grp/dca")[0])
        new_bit_map = self.set_bit_map(current_bit_map, dca, False)
        self.send_message(f"/bus/{str(bus).zfill(2)}/grp/dca", new_bit_map)
        logging.info(f" Removing bus {bus} to DCA {dca}")

    def clear_bus_dcas(self, bus: int):
        if(bus>16):
            logging.warning("Cannot control busses greater than 16.")
            return

        self.send_message(f"/bus/{str(bus).zfill(2)}/grp/dca", 0)
        logging.info(f" Removing bus {bus} from all DCAs")


    # Commands for DCAs
    def mute_dca(self, dca: int):
        if(dca>8):
            logging.warning("Cannot control DCAs greater than 8.")
            return
        self.send_message(f"/dca/{dca}/on", "OFF")
        logging.info(f" Muting DCA {dca}")

    def unmute_dca(self, dca: int):
        if(dca>8):
            logging.warning("Cannot control DCAs greater than 8.")
            return
        self.send_message(f"/dca/{dca}/on", "ON")
        logging.info(f" Unmuting DCA {dca}")

    def set_dca_fader(self, dca: int, value: float):
        if(dca>8):
            logging.warning("Cannot control DCAs greater than 8.")
            return
        self.send_message(f"/dca/{dca}/fader", value)
        logging.info(f" Setting DCA {dca} fader to {value}")

    def add_dca_to_dca(self, dca_channel: int, dca: int):
        if(dca_channel>8 or dca>8):
            logging.warning("Cannot control DCAs greater than 8.")
            return

        current_bit_map = int(self.get_peremeter(f"/dca/{dca_channel}/grp/dca")[0])
        new_bit_map = self.set_bit_map(current_bit_map, dca, True)
        self.send_message(f"/dca/{dca_channel}/grp/dca", new_bit_map)
        logging.info(f" Adding DCA {dca_channel} to DCA {dca}")