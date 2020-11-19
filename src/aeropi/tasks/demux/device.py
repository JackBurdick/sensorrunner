from .demux import Demux
from gpiozero import Device
from gpiozero.pins.mock import MockFactory
from gpiozero.pins.native import NativeFactory


"""
temporary file. this will eventually be replaced by a config driven setup

"""

# TODO: use only single pin lib
Device.pin_factory = NativeFactory()


def return_demux():
    INDEX_PINS = [25, 23, 24, 17]
    PWR_PIN = 27
    UNCONNECTED = [11, 12, 13, 14, 15]  # TODO: allow for manual off of pins
    CONNECTED = []
    ON_DURATION = 0.3

    demuxer_a = Demux(
        INDEX_PINS,
        PWR_PIN,
        connected=CONNECTED,
        unconnected=UNCONNECTED,
        on_duration=ON_DURATION,
    )
    return demuxer_a


DEMUX = return_demux()