import logging

from pythonosc import udp_client

class X32:
    def __init__(self, address):
        self.client = udp_client.SimpleUDPClient(address, 10023)

    def send_message(self, address, *args):
        self.client.send_message(address, args)

    # Mute and unmute commands for channels
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

    # Mute and unmute commands for auxins
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

    # Mute and unmute commands for busses
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

    # Mute and unmute commands for DCAs
    def mute_dca(self, dca: int):
        if(dca>8):
            logging.warning("Cannot control DCAs greater than 8.")
            return
        self.send_message(f"/dca/{dca}/on", "OFF")
        logging.info(f" Muting dca {dca}")

    def unmute_dca(self, dca: int):
        if(dca>8):
            logging.warning("Cannot control DCAs greater than 8.")
            return
        self.send_message(f"/dca/{dca}/on", "ON")
        logging.info(f" Unmuting dca {dca}")

    def set_dca_fader(self, dca: int, value: float):
        if(dca>8):
            logging.warning("Cannot control DCAs greater than 8.")
            return
        self.send_message(f"/dca/{dca}/fader", value)
        logging.info(f" Setting dca {dca} fader to {value}")