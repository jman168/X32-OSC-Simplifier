import logging

from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server
from bitarray import bitarray

import time

class X32:
    def __init__(self, address):
        self.disp = dispatcher.Dispatcher()
        self.disp.set_default_handler(print)
        self.server = osc_server.BlockingOSCUDPServer(("0.0.0.0", 10023), self.disp)
        self.client = udp_client.SimpleUDPClient(address, 10023)
        self.server.socket = self.client._sock

        logging.info(" Testing faders...")
        for i in range(1, 17):
            logging.debug(f" Testing channel {i}")
            self.test_fader(f"/ch/{str(i).zfill(2)}", False)
        for i in range(1, 9):
            logging.debug(f" Testing DCA {i}")
            self.test_fader(f"/dca/{i}", True)
        logging.info(" Done!")
        logging.info(" X32 Ready!")

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

    def test_fader(self, fader_path, is_dca):
        if is_dca:
            subpath = "/"
        else:
            subpath = "/mix/"
        
        mute_status = self.get_peremeter(fader_path+subpath+"on")[0]
        fader_pos = self.get_peremeter(fader_path+subpath+"fader")[0]
            
        self.send_message(fader_path+subpath+"on", "OFF")
        self.send_message(fader_path+subpath+"fader", 1.0)

        time.sleep(0.25)
        self.send_message(fader_path+subpath+"fader", 0.0)
        time.sleep(0.25)

        self.send_message(fader_path+subpath+"on", mute_status)
        self.send_message(fader_path+subpath+"fader", fader_pos)

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
        logging.info(f" Removing channel {channel} from DCA {dca}")

    def clear_channel_dcas(self, channel: int):
        if(channel>32):
            logging.warning("Cannot control channels greater than 32.")
            return

        self.send_message(f"/ch/{str(channel).zfill(2)}/grp/dca", 0)
        logging.info(f" Removing channel {channel} from all DCAs")

    def add_channel_to_group(self, channel: int, group: int):
        if(channel>32 or group>6):
            logging.warning("Cannot control channels greater than 32 or mute groups greater than 6.")
            return

        current_bit_map = int(self.get_peremeter(f"/ch/{str(channel).zfill(2)}/grp/mute")[0])
        new_bit_map = self.set_bit_map(current_bit_map, group, True)
        self.send_message(f"/ch/{str(channel).zfill(2)}/grp/mute", new_bit_map)
        logging.info(f" Adding channel {channel} to mute group {group}")

    def remove_channel_from_group(self, channel: int, group: int):
        if(channel>32 or group>6):
            logging.warning("Cannot control channels greater than 32 or mute groups greater than 6.")
            return

        current_bit_map = int(self.get_peremeter(f"/ch/{str(channel).zfill(2)}/grp/mute")[0])
        new_bit_map = self.set_bit_map(current_bit_map, group, False)
        self.send_message(f"/ch/{str(channel).zfill(2)}/grp/mute", new_bit_map)
        logging.info(f" Removing channel {channel} from mute group {group}")

    def clear_channel_groups(self, channel: int):
        if(channel>32):
            logging.warning("Cannot control channels greater than 32.")
            return

        self.send_message(f"/ch/{str(channel).zfill(2)}/grp/mute", 0)
        logging.info(f" Removing channel {channel} from all mute groups")


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
        logging.info(f" Removing auxin {auxin} from DCA {dca}")

    def clear_auxin_dcas(self, auxin: int):
        if(auxin>8):
            logging.warning("Cannot control auxins greater than 8.")
            return

        self.send_message(f"/auxin/{str(auxin).zfill(2)}/grp/dca", 0)
        logging.info(f" Removing auxin {auxin} from all DCAs")

    def add_auxin_to_group(self, auxin: int, group: int):
        if(auxin>8 or group>6):
            logging.warning("Cannot control auxins greater than 8 or mute groups greater than 6.")
            return

        current_bit_map = int(self.get_peremeter(f"/auxin/{str(auxin).zfill(2)}/grp/mute")[0])
        new_bit_map = self.set_bit_map(current_bit_map, group, True)
        self.send_message(f"/auxin/{str(auxin).zfill(2)}/grp/mute", new_bit_map)
        logging.info(f" Adding auxin {auxin} to mute group {group}")

    def remove_auxin_from_group(self, auxin: int, group: int):
        if(auxin>8 or group>6):
            logging.warning("Cannot control auxins greater than 8 or mute groups greater than 6.")
            return

        current_bit_map = int(self.get_peremeter(f"/auxin/{str(auxin).zfill(2)}/grp/mute")[0])
        new_bit_map = self.set_bit_map(current_bit_map, group, False)
        self.send_message(f"/auxin/{str(auxin).zfill(2)}/grp/mute", new_bit_map)
        logging.info(f" Removing auxin {auxin} from mute group {group}")

    def clear_auxin_groups(self, auxin: int):
        if(auxin>8):
            logging.warning("Cannot control auxins greater than 8.")
            return

        self.send_message(f"/auxin/{str(auxin).zfill(2)}/grp/mute", 0)
        logging.info(f" Removing auxin {auxin} from all mute groups")


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
        logging.info(f" Removing bus {bus} from DCA {dca}")

    def clear_bus_dcas(self, bus: int):
        if(bus>16):
            logging.warning("Cannot control busses greater than 16.")
            return

        self.send_message(f"/bus/{str(bus).zfill(2)}/grp/dca", 0)
        logging.info(f" Removing bus {bus} from all DCAs")

    def add_bus_to_group(self, bus: int, group: int):
        if(bus>16 or group>6):
            logging.warning("Cannot control busses greater than 16 or mute groups greater than 6.")
            return

        current_bit_map = int(self.get_peremeter(f"/bus/{str(bus).zfill(2)}/grp/mute")[0])
        new_bit_map = self.set_bit_map(current_bit_map, group, True)
        self.send_message(f"/bus/{str(bus).zfill(2)}/grp/mute", new_bit_map)
        logging.info(f" Adding bus {bus} to mute group {group}")

    def remove_bus_from_group(self, bus: int, group: int):
        if(bus>16 or group>6):
            logging.warning("Cannot control busses greater than 16 or mute groups greater than 6.")
            return

        current_bit_map = int(self.get_peremeter(f"/bus/{str(bus).zfill(2)}/grp/mute")[0])
        new_bit_map = self.set_bit_map(current_bit_map, group, False)
        self.send_message(f"/bus/{str(bus).zfill(2)}/grp/mute", new_bit_map)
        logging.info(f" Removing bus {bus} from mute group {group}")

    def clear_bus_groups(self, bus: int):
        if(bus>16):
            logging.warning("Cannot control busses greater than 16.")
            return

        self.send_message(f"/bus/{str(bus).zfill(2)}/grp/mute", 0)
        logging.info(f" Removing bus {bus} from all mute groups")


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